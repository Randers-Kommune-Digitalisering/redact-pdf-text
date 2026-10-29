"""Flask API endpoints for PDF redaction."""

import io
import json
import logging
import re
import tempfile
from pathlib import Path

import fitz  # PyMuPDF
from flask import Blueprint, jsonify, request, send_file

logger = logging.getLogger(__name__)
api_endpoints = Blueprint('api', __name__, url_prefix='/api')


def _ocr_pdf(input_pdf: bytes) -> bytes:
    """Add a Danish OCR text layer to a PDF."""
    import ocrmypdf

    with tempfile.TemporaryDirectory() as workdir:
        input_path = Path(workdir) / 'input.pdf'
        output_path = Path(workdir) / 'output.pdf'
        input_path.write_bytes(input_pdf)
        ocrmypdf.ocr(
            input_path,
            output_path,
            language=['dan'],
            deskew=True,
            rotate_pages=True,
        )
        return output_path.read_bytes()


@api_endpoints.route('/status', methods=['GET'])
def status():
    return jsonify({"success": True, "message": "API is up and running"})


@api_endpoints.route('/redact', methods=['POST'])
def redact_pdf():
    # Check if the request contains a file
    try:
        input_pdf = request.files['file'].read()
        logger.debug(f"Received PDF file of size: {len(input_pdf)} bytes")
    except Exception:
        return jsonify({"success": False, "message": "File not provided or invalid"}), 400

    # Check if the request contains regex pattern(s)
    try:
        regex_pattern = request.form.get('pattern')
    except Exception:
        return jsonify({"success": False, "message": "Regex pattern not provided"}), 400

    try:
        regex_pattern = json.loads(regex_pattern)

        if not isinstance(regex_pattern, list):
            raise ValueError("Regex pattern is not a valid JSON list")
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

    if not regex_pattern or not all(regex_pattern):
        return jsonify({"success": False, "message": "Regex pattern(s) invalid"}), 400

    replacement = request.form.get('replacement', None)

    # Load the PDF file
    try:
        doc = fitz.open(stream=input_pdf, filetype="pdf")
    except Exception:
        return jsonify({"success": False, "message": "Error loading PDF file"}), 400

    if any(not page.get_text("text").strip() for page in doc):
        doc.close()
        try:
            input_pdf = _ocr_pdf(input_pdf)
            doc = fitz.open(stream=input_pdf, filetype="pdf")
        except Exception:
            logger.error("OCR processing failed")
            return jsonify({"success": False, "message": "Error processing scanned PDF"}), 500

    output_stream = io.BytesIO()

    # Loop through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load the page

        # Extract the text and positioning using re.search
        text_instances = []
        text = page.get_text("text")

        for pattern in regex_pattern:
            if pattern.endswith('/regex'):
                pattern = pattern[:-6]
                for match in re.finditer(pattern, text):
                    text_instances.extend(page.search_for(match.group()))
            else:
                # Treat as string
                text_instances.extend(page.search_for(pattern))

        for instance in text_instances:
            if page.get_text('text', clip=instance) == "":
                continue

            # Add a redact annotation over the found area (position)
            # Adjust the height of the redaction annotation
            rect = fitz.Rect(instance.x0, instance.y0 + 5, instance.x1, instance.y1 - 3)
            page.add_redact_annot(rect, fill=(1, 0, 0))  # Set redaction color to red (RGB)
            page.apply_redactions()

            # Add a text annotation to overlay the redacted text
            if replacement:
                page.insert_text(instance[:2], replacement, fontsize=12, color=(0, 0, 0))

        # Apply the redactions (remove or replace the matched text)
        page.apply_redactions()

    # Save the modified PDF to the output stream
    doc.save(output_stream)
    output_stream.seek(0)

    return send_file(output_stream, as_attachment=True, download_name='redacted.pdf', mimetype='application/pdf')

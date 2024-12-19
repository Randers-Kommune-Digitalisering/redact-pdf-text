import logging
import fitz  # PyMuPDF
import re
import base64
import json

from flask import Blueprint, jsonify
from flask import request, send_file
import io

logger = logging.getLogger(__name__)
api_endpoints = Blueprint('api', __name__, url_prefix='/api')


@api_endpoints.route('/status', methods=['GET'])
def status():
    return jsonify({"success": True, "message": "API is up and running"})


@api_endpoints.route('/redact', methods=['POST'])
def redact_pdf():
    try:
        input_pdf = request.files['file'].read()
        logger.info(f"Received PDF file of size: {len(input_pdf)} bytes")
    except Exception as e:
        return jsonify({"success": False, "message": "File not provided or invalid"}), 400

    try:
        regex_pattern = request.form.getlist('pattern')
    except Exception as e:
        return jsonify({"success": False, "message": "Regex pattern not provided or invalid"}), 400

    if not isinstance(regex_pattern, list):
        regex_pattern = [regex_pattern]
    
    replacement = request.form.get('replacement', None)

    try:
        doc = fitz.open(stream=input_pdf, filetype="pdf")
        output_stream = io.BytesIO()
    except Exception as e:
        return jsonify({"success": False, "message": "Error loading PDF file"}), 400

    # Loop through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load the page

        # Extract the text and positioning using re.search
        text_instances = []
        text = page.get_text("text")

        for pattern in regex_pattern:
            for match in re.finditer(pattern, text):
                text_instances.extend(page.search_for(match.group()))

        for instance in text_instances:
            if page.get_text('text', clip=instance) == "":
                continue

            # Add a redact annotation over the found area (position)
            page.add_redact_annot(instance)
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

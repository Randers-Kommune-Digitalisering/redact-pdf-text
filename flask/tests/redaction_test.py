"""Tests for PDF redaction and OCR preprocessing."""

import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import fitz
import pytest
from flask.testing import FlaskClient
from flask.wrappers import Response

import api_endpoints
from api_endpoints import _ocr_pdf
from main import create_app


@pytest.fixture()
def client() -> FlaskClient:
    app = create_app()
    app.config.update({'TESTING': True})
    return app.test_client()


def _create_pdf(text: str | None = None) -> bytes:
    document = fitz.open()
    page = document.new_page()
    if text:
        page.insert_text((72, 72), text)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def _create_scanned_pdf() -> bytes:
    document = fitz.open()
    page = document.new_page()
    image = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 10, 10))
    image.clear_with(255)
    page.insert_image(page.rect, pixmap=image)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def _redact(client: FlaskClient, pdf_bytes: bytes) -> Response:
    return client.post(
        '/api/redact',
        data={
            'file': (io.BytesIO(pdf_bytes), 'document.pdf'),
            'pattern': json.dumps(['secret']),
        },
        content_type='multipart/form-data',
    )


def test_scanned_pdf_is_ocr_processed_before_redaction(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(api_endpoints, '_ocr_pdf', lambda _: _create_pdf('secret'))

    response = _redact(client, _create_scanned_pdf())

    assert response.status_code == 200
    with fitz.open(stream=response.data, filetype='pdf') as document:
        assert 'secret' not in document[0].get_text()


def test_pdf_with_text_layer_skips_ocr(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(api_endpoints, '_ocr_pdf', lambda _: pytest.fail('OCR should be skipped'))

    response = _redact(client, _create_pdf('secret'))

    assert response.status_code == 200
    with fitz.open(stream=response.data, filetype='pdf') as document:
        assert 'secret' not in document[0].get_text()


def test_ocr_failure_returns_generic_error(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_ocr(_: bytes) -> bytes:
        raise RuntimeError('sensitive error details')

    monkeypatch.setattr(api_endpoints, '_ocr_pdf', fail_ocr)

    response = _redact(client, _create_scanned_pdf())

    assert response.status_code == 500
    assert response.get_json() == {
        'success': False,
        'message': 'Error processing scanned PDF',
    }


def test_ocr_pdf_uses_danish_and_cleans_up_temporary_files(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_pdf = _create_pdf()
    call = {}

    def fake_ocr(
        input_file: Path,
        output_file: Path,
        *,
        language: list[str],
        deskew: bool,
        rotate_pages: bool,
    ) -> None:
        call.update(
            input_path=input_file,
            output_path=output_file,
            language=language,
            deskew=deskew,
            rotate_pages=rotate_pages,
        )
        output_file.write_bytes(input_file.read_bytes())

    monkeypatch.setitem(sys.modules, 'ocrmypdf', SimpleNamespace(ocr=fake_ocr))

    assert _ocr_pdf(input_pdf) == input_pdf
    assert call['language'] == ['dan']
    assert call['deskew'] is True
    assert call['rotate_pages'] is True
    assert not call['input_path'].exists()
    assert not call['output_path'].exists()

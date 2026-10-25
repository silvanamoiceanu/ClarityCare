"""Runtime checks using real PDF/image libraries and Streamlit's test runner."""
from pathlib import Path
import io
import unittest
from unittest.mock import patch

import fitz
from PIL import Image
from streamlit.testing.v1 import AppTest

from claritycare.documents import extract_document


class UploadRuntimeTests(unittest.TestCase):
    def pdf(self, text=None, pages=1):
        with fitz.open() as document:
            for _ in range(pages):
                page = document.new_page()
                if text:
                    page.insert_text((72, 72), text)
            return document.tobytes()

    def test_short_text_pdf_does_not_need_ocr(self):
        with patch("claritycare.documents.ocr_image", side_effect=AssertionError("Unexpected OCR")):
            text = extract_document(self.pdf("Billing 800-555-1234"), "bill.pdf")
        self.assertIn("[Page 1]", text)
        self.assertIn("800-555-1234", text)

    def test_image_only_pdf_uses_ocr(self):
        with patch("claritycare.documents.ocr_image", return_value="Scanned bill") as ocr:
            text = extract_document(self.pdf(), "scan.pdf")
        ocr.assert_called_once()
        self.assertIn("Scanned bill", text)

    def test_image_upload_uses_ocr(self):
        image = io.BytesIO()
        Image.new("RGB", (100, 100), "white").save(image, format="PNG")
        with patch("claritycare.documents.ocr_image", return_value="Image bill"):
            self.assertIn("Image bill", extract_document(image.getvalue(), "bill.png"))

    def test_pdf_page_limit(self):
        with self.assertRaisesRegex(ValueError, "20 pages"):
            extract_document(self.pdf(pages=21), "long.pdf")

    def test_blank_scan_has_actionable_error(self):
        with patch("claritycare.documents.ocr_image", return_value=""):
            with self.assertRaisesRegex(ValueError, "No readable text"):
                extract_document(self.pdf(), "blank.pdf")

    def test_interface_renders_without_credentials(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "", "SERPER_API_KEY": ""}):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "src/claritycare/ui.py")).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Less confusion. More clarity.")

    def test_clear_session_discards_document(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "src/claritycare/ui.py"))
        app.session_state["text"] = "Private document fixture"
        app.session_state["explanation"] = {"summary": "Private summary"}
        app.run(timeout=30)
        app.button[0].click().run(timeout=30)
        self.assertNotIn("text", app.session_state)
        self.assertNotIn("explanation", app.session_state)
        self.assertEqual(len(app.exception), 0)


if __name__ == "__main__":
    unittest.main()

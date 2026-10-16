import unittest
from unittest.mock import patch
from claritycare.documents import extract_contacts, extract_document, validate_explanation, search_contact_help


class DocumentTests(unittest.TestCase):
    def test_phone_evidence_and_extension(self):
        result = extract_contacts("[Page 2]\nBilling: (800) 555-1234 ext. 42\nFax: 800-555-9999")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["dial"], "+18005551234;ext=42")
        self.assertEqual(result[0]["page"], 2)
        self.assertEqual(result[0]["evidence"], "Billing: (800) 555-1234 ext. 42")
        self.assertTrue(result[1]["label"].startswith("Fax"))

    def test_no_phone_is_not_invented(self):
        self.assertEqual(extract_contacts("[Page 1]\nAmount due $123.45"), [])

    def test_different_labels_preserved(self):
        self.assertEqual(len(extract_contacts("Billing 800-555-1234\nMember services 800-555-1234")), 2)

    def test_unlabelled_candidate(self):
        self.assertIn("confirm", extract_contacts("8005551234")[0]["label"])

    def test_upload_limits_and_types(self):
        for data, name in ((b"", "a.pdf"), (b"x" * (10 * 1024 * 1024 + 1), "a.pdf"), (b"x", "a.exe")):
            with self.assertRaises(ValueError):
                extract_document(data, name)

    def test_unsupported_quotes_removed(self):
        result = validate_explanation({
            "summary": "A benefits statement.", "document_type": "EOB",
            "key_details": [{"fact": "Insurance paid $20.", "source_quote": "Paid $20"},
                            {"fact": "You owe $50.", "source_quote": "Amount due $50"}],
            "terms": [], "next_steps": [], "uncertainties": []
        }, "[Page 1]\nPaid $20")
        self.assertEqual(len(result["key_details"]), 1)
        self.assertEqual(len(result["uncertainties"]), 1)

    def test_malformed_model_response(self):
        for result in ([], {}, {"summary": None}):
            with self.assertRaises(ValueError):
                validate_explanation(result, "")

    def test_search_needs_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "SERPER_API_KEY"):
                search_contact_help("Example Hospital")


if __name__ == "__main__":
    unittest.main()

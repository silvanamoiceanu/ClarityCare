# Clarity Care document interface

A Streamlit interface alongside the existing CrewAI command-line workflow.

## Run locally

Use Python 3.10–3.13. From the repository root:

```bash
python -m pip install -r requirements-ui.txt
cp .env.example .env
streamlit run src/claritycare/ui.py
```

Set OPENAI_API_KEY in .env for explanations. CLARITYCARE_MODEL defaults to
gpt-4o-mini, already used by this repository. Optionally set SERPER_API_KEY
for public contact research.

Scanned PDFs and photos require the Tesseract executable:
macOS: `brew install tesseract`; Ubuntu: `sudo apt-get install tesseract-ocr`.
Text PDFs do not require Tesseract. OCR currently uses English.

## Behavior and limits

Accepts PDF, PNG, JPEG up to 10 MB; 20 PDF pages; 25 megapixels per uploaded
image; 60,000 extracted characters. Unlock encrypted PDFs before uploading.

Documents are read in server memory without an application document database.
Explanation requires explicit consent to send extracted text to the AI provider.
Eighth-grade reading level is a writing target, not a measured score.
Fact cards require exact source excerpts; this does not prove interpretations.
Users should check important facts and OCR against their original document.

Phone candidates include page labels and evidence. Fax candidates have no call
button. Unlabelled candidates require confirmation because account identifiers
can resemble phone numbers. Labels are inferred from the same text line.

Public research sends only the organization name entered separately by the user.
Search snippets and menu tips are unverified leads with source links.
No calls are placed and no universal phone-menu bypass is promised.

Clear my session clears application results and resets the upload widget.
It does not erase previous API requests or provider logs. Browser, server, and
AI provider infrastructure have their own retention behavior. Do not enable
prompt/debug logging. Configure authentication, HTTPS, and provider data controls
before hosting sensitive documents. This change does not establish HIPAA compliance.

UI dependencies are separate so the existing CrewAI lockfile remains usable.
Install requirements-ui.txt for the interface.

## Verification

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

CI checks compilation and document unit tests without API credentials.
Manual checks still needed: text PDF, scanned PDF, photo, missing credentials,
AI explanation with real credentials, phone links, public sources, replacement
uploads, and clearing the session.

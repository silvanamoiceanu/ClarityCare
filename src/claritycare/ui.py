"""Run: streamlit run src/claritycare/ui.py"""
import hashlib
import logging
import os

import streamlit as st
from dotenv import load_dotenv
from claritycare.documents import extract_document, extract_contacts, explain_document, search_contact_help

load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"
for name in ("crewai", "LiteLLM", "litellm"):
    logging.getLogger(name).setLevel(logging.CRITICAL)

st.set_page_config(page_title="Clarity Care", page_icon="🌿", layout="wide")
st.markdown("""
<style>
.stApp {background:#f6f8f5}
.block-container {max-width:1120px;padding-top:2.5rem}
h1,h2,h3 {color:#173e35}
[data-testid="stFileUploader"] {background:white;border-radius:16px;padding:1rem}
</style>
""", unsafe_allow_html=True)
st.caption("CLARITY CARE / YOUR DOCUMENT COMPANION")
st.title("Less confusion. More clarity.")
st.write("Understand your healthcare paperwork and prepare to reach a real person.")
with st.sidebar:
    st.subheader("Your document, explained")
    st.write("1. Upload your document.\n\n2. Read a plain-language explanation.\n\n3. Find contacts and prepare your call.")
    st.caption("Uploads are processed in server memory without an application document database. "
               "Explain sends extracted text to the AI provider. Public search sends only the organization name you enter.")
    if st.button("Clear my session"):
        version = st.session_state.get("version", 0) + 1
        st.session_state.clear()
        st.session_state["version"] = version
        st.rerun()

st.subheader("Start with your document")
st.caption("PDF, PNG, or JPG · Up to 10 MB · Up to 20 PDF pages")
upload = st.file_uploader("Choose a document", type=["pdf", "png", "jpg", "jpeg"],
                          key=f"upload_{st.session_state.get('version', 0)}")
st.caption("AI explanations and scan text may contain mistakes. Compare important details with your original document.")

if upload is not None:
    data = upload.getvalue()
    fingerprint = hashlib.sha256(data).hexdigest()
    if st.session_state.get("fingerprint") != fingerprint:
        for key in ("text", "contacts", "explanation", "search_results"):
            st.session_state.pop(key, None)
        st.session_state["fingerprint"] = fingerprint
    if "text" not in st.session_state:
        try:
            with st.spinner("Reading your document…"):
                text = extract_document(data, upload.name)
                st.session_state["text"] = text
                st.session_state["contacts"] = extract_contacts(text)
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Could not read this file. Try an unlocked PDF or clear image. Scans require Tesseract on the server.")
    if "text" in st.session_state:
        text = st.session_state["text"]
        understand, contacts_tab, original = st.tabs(["Understand my document", "Reach a person", "Check source text"])
        with understand:
            st.subheader("Your paperwork, in everyday language")
            st.write("Get an explanation written for an eighth-grade reading level.")
            consent = st.checkbox("I agree to send this document's extracted text to the AI provider.",
                                  key="consent_" + fingerprint)
            if st.button("Explain my document", type="primary", disabled=not consent):
                st.session_state.pop("explanation", None)
                try:
                    with st.spinner("Putting your document into plain language…"):
                        st.session_state["explanation"] = explain_document(text)
                except ValueError as exc:
                    st.error(str(exc))
                except Exception:
                    st.error("The explanation service is unavailable. Check server credentials or try again. Extracted contacts remain available.")
            explanation = st.session_state.get("explanation")
            if explanation:
                st.caption(explanation["document_type"])
                st.write(explanation["summary"])
                st.subheader("Key details")
                for detail in explanation["key_details"]:
                    with st.container(border=True):
                        st.write(detail["fact"])
                        st.caption("From your document: " + detail["source_quote"])
                if explanation["terms"]:
                    with st.expander("What do these words mean?"):
                        for term in explanation["terms"]:
                            st.write(term["term"] + ": " + term["meaning"])
                st.subheader("What you can do next")
                for step in explanation["next_steps"]:
                    st.write("• " + step)
                if explanation["uncertainties"]:
                    st.subheader("What needs a closer look")
                    for issue in explanation["uncertainties"]:
                        st.write("• " + issue)
                report = explanation["summary"] + "\n\nNext steps\n" + "\n".join(explanation["next_steps"])
                st.download_button("Download explanation", report, "clarity-care-explanation.txt", "text/plain")
        with contacts_tab:
            st.subheader("Find the number on your bill")
            st.caption("Numbers come from extracted text. Confirm against the original, especially after scanning.")
            contacts = st.session_state["contacts"]
            if not contacts:
                st.info("No phone numbers found. Check the original or the organization's official contact page.")
            for contact in contacts:
                with st.container(border=True):
                    st.write(contact["label"])
                    st.write(contact["number"])
                    st.caption(f"Page {contact['page']} · " + contact["evidence"])
                    if not contact["label"].startswith("Fax"):
                        st.link_button("Call this number", "tel:" + contact["dial"])
            st.subheader("Prepare to speak with someone")
            st.write('When voice requests are accepted, try “billing representative” or “speak to a person.” '
                     "These are general suggestions. There is no guaranteed shortcut for every phone system.")
            st.text_area("A script you can use",
                         "Hi, I need help understanding a document I received. Can you connect me with billing or claims? "
                         "Please explain the charges, what insurance covered, and whether I owe anything. "
                         "Can you send an itemized statement?", height=130)
            st.caption("Have your document ready. Share personal details only after confirming you reached the right organization.")
            st.subheader("Look for public contact and phone-menu help")
            with st.form("public_search"):
                provider = st.text_input("Provider or insurer name", max_chars=160)
                st.caption("Enter only the public organization name. Do not enter patient names, account numbers, or medical details.")
                submit = st.form_submit_button("Find contact help")
            if submit:
                st.session_state.pop("search_results", None)
                try:
                    with st.spinner("Looking for public contact information…"):
                        st.session_state["search_results"] = search_contact_help(provider)
                except ValueError as exc:
                    st.error(str(exc))
                except Exception:
                    st.error("Search is unavailable. Try the organization's official website.")
            if "search_results" in st.session_state:
                st.warning("These search results are unverified leads. Prefer official websites. Confirm direct numbers and menu sequences.")
                if not st.session_state["search_results"]:
                    st.info("No results found. Use the number printed on your document.")
                for item in st.session_state["search_results"]:
                    with st.container(border=True):
                        st.write(item.get("title", "Contact information"))
                        st.write(item.get("snippet", ""))
                        st.link_button("Open source", item["link"])
        with original:
            st.subheader("Text read from your document")
            st.write("Compare page labels and source excerpts with your original file.")
            st.text_area("Extracted text", text, height=500, disabled=True)
else:
    for column, title, body in zip(st.columns(3),
        ["01 · Understand", "02 · Know what matters", "03 · Get connected"],
        ["Plain-language explanations of your healthcare paperwork.",
         "Important details linked to excerpts from your document.",
         "Billing contacts and help preparing your conversation."]):
        with column:
            st.subheader(title)
            st.write(body)

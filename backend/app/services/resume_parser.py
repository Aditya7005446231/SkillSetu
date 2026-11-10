import pymupdf

def extract_resume_text(file_bytes: bytes) -> str:
    """Extract text from a PDF resume."""

    with pymupdf.open(stream=file_bytes, filetype="pdf") as document:
        text = "\n".join(page.get_text() for page in document)

    if not text.strip():
        raise ValueError(
            "No readable text found. This may be a scanned PDF."
        )

    return text
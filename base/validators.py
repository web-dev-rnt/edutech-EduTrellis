"""Upload validators: check what a file really is, not just what it is called."""
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible

VIDEO_EXTENSIONS = ["mp4", "webm", "mov", "m4v", "mkv"]
MAX_PDF_BYTES = 100 * 1024 * 1024


@deconstructible
class PdfContentValidator:
    """Reject files that are not real PDFs (e.g. an .html or .exe renamed to .pdf)."""

    def __call__(self, upload):
        if upload.size and upload.size > MAX_PDF_BYTES:
            raise ValidationError("PDF files must be 100 MB or smaller.")
        position = upload.tell() if hasattr(upload, "tell") else 0
        try:
            upload.seek(0)
            header = upload.read(1024)
        finally:
            upload.seek(position)
        if b"%PDF-" not in header:
            raise ValidationError("This file is not a valid PDF.")

    def __eq__(self, other):
        return isinstance(other, PdfContentValidator)


validate_pdf_content = PdfContentValidator()
validate_video_extension = FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)

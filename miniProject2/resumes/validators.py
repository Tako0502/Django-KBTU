from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.docx', '.doc']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Please upload a PDF or DOCX file.') 
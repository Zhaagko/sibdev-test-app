import io
import csv
from django.core.files.uploadedfile import UploadedFile


def uploaded_file_to_csv_reader(uploaded_file: UploadedFile) -> csv.DictReader:
    file_bytes = uploaded_file.read()
    file_string = io.StringIO(file_bytes.decode("utf-8"))
    reader = csv.DictReader(file_string)
    return reader


def deserialize_uploaded_csv_file(uploaded_file: UploadedFile) -> list[dict]:
    reader = uploaded_file_to_csv_reader(uploaded_file)
    reader_lines = list(reader)
    return reader_lines

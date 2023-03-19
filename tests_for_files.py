import zipfile
import os
import pytest
from PyPDF2 import PdfReader
from openpyxl import load_workbook

DIRECTORY = 'resources'
ARCHIVE_PATH = f'{DIRECTORY}/archive.zip'
XLSX_PATH = f'{DIRECTORY}/example.xlsx'
PDF_PATH = f'{DIRECTORY}/file.pdf'
CSV_PATH = f'{DIRECTORY}/username.csv'


@pytest.fixture()
def create_zip():
    file_dir = os.listdir(DIRECTORY)
    with zipfile.ZipFile(ARCHIVE_PATH, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in file_dir:
            add_file = os.path.join(DIRECTORY, file)
            zf.write(add_file)


def xlsx_size_meter(file):
    workbook = load_workbook(file)
    sheet = workbook.active
    return sheet.max_row, sheet.max_column


def pdf_pages_counter(file):
    reader = PdfReader(file)
    return len(reader.pages)


def test_csv(create_zip):
    with open(CSV_PATH, 'r') as csv_file:
        csv_row = len(list(csv_file))
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as zf:
        with zf.open(CSV_PATH) as archive_csv_file:
            archive_csv_row = len(list(archive_csv_file))
    assert archive_csv_row == csv_row
    os.remove(ARCHIVE_PATH)


def test_pdf(create_zip):
    pdf_pages = pdf_pages_counter(PDF_PATH)
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as zf:
        with zf.open(PDF_PATH) as archive_pdf_file:
            archive_pdf_pages = pdf_pages_counter(archive_pdf_file)
    assert archive_pdf_pages == pdf_pages
    os.remove(ARCHIVE_PATH)


def test_xlsx(create_zip):
    xlsx_row, xlsx_column = xlsx_size_meter(XLSX_PATH)
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as zf:
        with zf.open(XLSX_PATH) as archive_xlsx_file:
            archive_xlsx_row, archive_xlsx_column = xlsx_size_meter(archive_xlsx_file)
    assert archive_xlsx_row == xlsx_row and archive_xlsx_column == xlsx_column
    os.remove(ARCHIVE_PATH)

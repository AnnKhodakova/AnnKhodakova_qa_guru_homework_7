import zipfile
import os
from PyPDF2 import PdfReader
from openpyxl import load_workbook

DIRECTORY = 'resources'
ARCHIVE_PATH = f'{DIRECTORY}/archive.zip'
XLSX_PATH = f'{DIRECTORY}/example.xlsx'
PDF_PATH = f'{DIRECTORY}/file.pdf'
CSV_PATH = f'{DIRECTORY}/username.csv'


def create_zip():
    file_dir = os.listdir(DIRECTORY)
    with zipfile.ZipFile(ARCHIVE_PATH, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in file_dir:
            add_file = os.path.join(DIRECTORY, file)
            zf.write(add_file)


def converting_xlsx_to_list(file):
    workbook = load_workbook(file)
    sheet = workbook.active
    max_row = sheet.max_row
    max_column = sheet.max_column
    xlsx_list = []
    for row_index in range(1, max_row + 1):
        row = []
        for column_index in range(1, max_column + 1):
            row.append(sheet.cell(row=row_index, column=column_index).value)
        xlsx_list.append(row)
    return xlsx_list


def converting_pdf_to_string(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text


def test():
    create_zip()
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as zf:
        with zf.open(XLSX_PATH) as archive_xlsx_file:
            archive_xlsx_list = converting_xlsx_to_list(archive_xlsx_file)
            xlsx_list = converting_xlsx_to_list(XLSX_PATH)
            assert archive_xlsx_list == xlsx_list
        with zf.open(PDF_PATH) as archive_pdf_file:
            archive_pdf_text = converting_pdf_to_string(archive_pdf_file)
            pdf_text = converting_pdf_to_string(PDF_PATH)
            assert archive_pdf_text == pdf_text
        with open(CSV_PATH) as csv_file:
            archive_csv_table = zf.read(CSV_PATH).decode("utf-8")
            csv_table = csv_file.read()
            assert archive_csv_table == csv_table

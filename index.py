import os
import fitz  # PyMuPDF
import re
from dotenv import load_dotenv

load_dotenv()

pdf_folder = os.getenv("PDF_FOLDER")
pdf_files_read = []
pdf_files_number = []
pdf_files_counter = 0
found_in_general = False

search_term = input('Type the term to look for in PDF files: ')
if search_term == "":
    search_term = os.getenv("DEFAULT_SEARCH_TERM")


def extract_and_pdf_files_number(pdf_file_name):
    pdf_file_splited = pdf_file_name.split("-", 1)[0]
    number = re.findall(r'\d+', pdf_file_splited)
    number = list(map(int, number))
    pdf_files_number.append(number)

def search_text_in_pdf(pdf_path, search_term):
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if search_term.lower() in text.lower():
                return True, page_num + 1
        return False, None
    except Exception as e:
        print(f'\nReading error in {pdf_path}: {e}')
        return False, None

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_files_read.append(filename)
        pdf_path = os.path.join(pdf_folder, filename)
        found, page = search_text_in_pdf(pdf_path, search_term)
        pdf_files_counter += 1
        if found:
            found_in_general = True
            print(f'>>> Term "{search_term}" found in "{filename}" on page {page} <<<')

if found_in_general == False:
    print(f'\nTerm "{search_term}" NOT found!')

for pdf_file in pdf_files_read:
  extract_and_pdf_files_number(pdf_file)

sorted_pdf_files_read = sorted(pdf_files_number)

last_pdf_file_read = sorted_pdf_files_read[-1][0]

print(f'\n{pdf_files_counter} PDF files read.')

print(f'\nLast PDF downloaded: {last_pdf_file_read}.')
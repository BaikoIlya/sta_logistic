import json
import os
import re
from PyPDF2 import PdfReader, PdfWriter


def main():
    files_list = [
        file_name for file_name in os.listdir('test_case')
        if file_name.endswith('.pdf')
    ]
    nums_and_files = []
    for pdf_doc in files_list:
        reader = PdfReader(f"test_case/{pdf_doc}")
        first_page = reader.pages[0]
        text = first_page.extract_text()
        group = re.search("Номер (\d*)", text)
        nums_and_files.append((int(group[1]), pdf_doc))
    writer = PdfWriter()
    for el in sorted(nums_and_files, key=lambda x: x[0]):
        reader = PdfReader(f"test_case/{el[1]}")
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(reader.metadata)
    with open("pack_1.pdf", "wb") as fp:
        writer.write(fp)
    result = {
        "name": "pack_1.pdf",
        "files_list": files_list
    }
    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

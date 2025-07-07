"""PDF Reader"""

import os
from os import listdir
from os.path import isfile, join
from pypdf import PdfReader

def verify_txt(name: str) -> bool:
    '''docstring'''
    file_path = f"./pdfs/{name}.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {file_path}")
        return True
    else:
        print(f"{file_path} does not exist")
        return False

# List all the pdf files in the directory
onlypdfs = [
    f for f in listdir("./pdfs/") if isfile(join("./pdfs/", f)) and f.endswith(".pdf")
]
print(onlypdfs)

# Loop through all the pdf files
for i in onlypdfs:
    try:
        verify_txt(f"{i}")
        # Creating a pdf reader object
        reader = PdfReader(f"./pdfs/{i}")

        # Printing number of pages in pdf file
        print(len(reader.pages))

        # Creating a page object
        for j in range(len(reader.pages)):
            page = reader.pages[j]
            # print(page.extract_text())

            # Writing the text to a file
            try:
                [[file.write(page.extract_text())] for file in open(f"./pdfs/{i}.txt", "w")]
            except Exception as e:
             print(e)
             continue
    except Exception as e:
        print(e)
        continue

'''docstring'''

import os
from os import listdir
from os.path import isfile, join
from pypdf import PdfReader
# import pandas as pd
import pytesseract

help(pytesseract)

# clientes = pd.read_csv("clientes.csv", sep=";")

'''onlypdfs = [
    f for f in listdir("./pdfs/") if isfile(join("./pdfs/", f)) and f.endswith(".pdf")
]
print(onlypdfs)

for i in onlypdfs:
    reader = PdfReader(f"./pdfs/{i}")

    print(len(reader.pages))

    for j in range(len(reader.pages)):
        page = reader.pages[j]
        print(page.extract_text())'''
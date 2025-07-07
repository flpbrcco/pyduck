"""
PDF Reader
"""
import pandas as pd # Import necessary libraries
from pdfreader import PDFDocument, SimplePDFViewer  # Import necessary libraries

path = "./pdfs/clientes_completo.pdf"   # Path to the PDF file

fd = open(path, "rb")   # Open the PDF file in binary mode
viewer = SimplePDFViewer(fd)    # Create a PDF viewer object

viewer.navigate(8)
viewer.render()   # Render the PDF page
page_8_canvas = viewer.canvas
print(page_8_canvas)   # Print the strings on the page

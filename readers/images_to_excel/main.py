'''Manipulação de imagens para inserção em banco de dados no formato xlsx
Tecnologias: Python, OpenCV, Pandas, Pillow'''

import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image

# Caminho da pasta com as imagens
folder_path = r'C:\Users\filip\OneDrive\Imagens\bazar'
# Nome do arquivo Excel de saída
output_file = 'produtos.xlsx'

# Cria um novo workbook e seleciona a planilha ativa
wb = Workbook()
ws = wb.active
ws.append(['Imagem', 'Nome do Arquivo', 'Formato', 'Largura', 'Altura'])  # Cabeçalho

row = 2  # Começa na segunda linha (primeira é o cabeçalho)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(folder_path, filename)
        with Image.open(image_path) as img:
            formato = img.format
            largura, altura = img.size

        # Adiciona os dados na planilha
        ws.append([None, filename, formato, largura, altura])

        # Adiciona a imagem na primeira coluna da linha atual
        img_for_excel = XLImage(image_path)
        img_for_excel.width = 80   # Ajuste o tamanho conforme necessário
        img_for_excel.height = 80
        ws.add_image(img_for_excel, f'A{row}')
        row += 1

# Ajusta a largura da coluna para exibir as imagens
ws.column_dimensions['A'].width = 15

# Salva o arquivo Excel
wb.save(output_file)
print(f'Arquivo {output_file} criado com sucesso!')

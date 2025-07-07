'''docstring'''
import pandas as pd

path = "./utils/Process Metadados.xlsx"

# Leitura Excel
df = pd.read_excel(path,  sheet_name="Fila", engine="openpyxl", header=None)

# Print dataframe
# print(f'{df}\n')
# print(f'{df[0][0]}\n')

'''for i in df:
    for j in df:
        if df[i][j] != "":
            print(f"Linha: {i}, Coluna: {j} \n {df[i][j]} \n ")
        else:
            break'''

# Índices True/False. Busca-se false para obter a posição com valor.
# nan_indices = df.isna()
print(df.loc[0][0])

# print(nan_indices)
# print(nan_indices[0])

'''for i in nan_indices:
    if not i:
        print(f'Encontrado: {i} \n')
        break
    else:
        print(f'Não encontrado {i} \n')
'''

def capture():
    '''busca da próxima linha com valor'''
    for i in nan_indices:
        if not i:
            break
    return i



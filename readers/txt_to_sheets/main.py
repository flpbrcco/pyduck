"""docstring"""

import pandas as pd

in_txt = "./docs/clientes.TXT"
out_xlsx = "./docs/out.xlsx"

df = pd.read_csv(in_txt, sep="\t", encoding="utf-8")

print(df.head())

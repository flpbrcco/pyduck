"""My First App
Here is our first attempt at using data to create a table:"""

import streamlit as st
import pandas as pd
import numpy as np

st.write("Here is our first attempt at using data to create a table: ")

st.write(
    pd.DataFrame({"primeira coluna": [1, 2, 3, 4], "segunda coluna": [10, 20, 30, 40]})
)

dataframe = pd.DataFrame(
    np.random.randn(10,20),
    columns = ('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
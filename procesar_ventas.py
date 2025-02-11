"""importacion de pandas"""
import pandas as pd

file_path = "datos_ventas.xlsx"
df = pd.read_excel(file_path)

print(df.head())

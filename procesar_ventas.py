"""importacion de pandas"""
import pandas as pd


# 📌 Cargando el archivo
file_path = "datos_ventas.xlsx"
df = pd.read_excel(file_path)

# 📌 Revisar si hay valores nulos
print("\nValores nulos por columna:")
print(df.isnull().sum())

# 📌 Convertir 'Fecha' a formato datetime
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# 📌 Eliminar filas donde 'Fecha' es NaT
df = df.dropna(subset=["Fecha"])

# 📌 Completar valores faltantes en 'Total_Venta' de forma segura
df.loc[df["Total_Venta"].isna(), "Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

# 📌 Filtrar solo ventas del año 2023
df_2023 = df[df["Fecha"].dt.year == 2023].copy()

# 📌 Agregar columna 'Mes'
df_2023["Mes"] = df_2023["Fecha"].dt.month

# 📌 Calcular total de ventas por vendedor
ventas_por_vendedor = df_2023.groupby("Vendedor")["Total_Venta"].sum().reset_index()
ventas_por_vendedor.rename(columns={"Total_Venta": "Total_Ventas"}, inplace=True)

# 📌 Calcular total de ventas por mes
ventas_por_mes = df_2023.groupby("Mes")["Total_Venta"].sum().reset_index()
ventas_por_mes.rename(columns={"Total_Venta": "Total_Ventas"}, inplace=True)

# 📌 Mostrar los resultados
print("\nTotal de ventas por vendedor:")
print(ventas_por_vendedor)

print("\nTotal de ventas por mes:")
print(ventas_por_mes)

# 📌 Creamos el archivo Excel con los resultados, para eso usamos la libreria xlsxwriter
output_file = "resumen_ventas.xlsx"

with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    ventas_por_vendedor.to_excel(writer, sheet_name="Resumen_Ventas", index=False)
    ventas_por_mes.to_excel(writer, sheet_name="Ventas_Mensuales", index=False)

print(f"\n✅ Archivo '{output_file}' generado correctamente.")

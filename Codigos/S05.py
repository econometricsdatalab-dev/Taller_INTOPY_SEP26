# -*- coding: utf-8 -*-
"""
Taller: Introducción a Python 
Tema: principios de gráficos y ejemplos de datos para econometría
Sesión: 05
Fecha: 19/09/2026
Docente: Alexis Adonai Morales Alberto
"""

# Instalación de modulos (ejecutar en caso de no tener el modulo)

pip install numpy pandas matplotlib
pip install geopandas
pip install datetime

# Modulo a importar/cargar 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime

# Pipeline 

def cargar(ruta: str) -> pd.DataFrame:
    if ruta.endswith(".csv"):
        return pd.read_csv(ruta, parse_dates=["fecha"])
    return pd.read_excel(ruta)
 
 
def limpiar(d: pd.DataFrame) -> pd.DataFrame:
    return (
        d.drop_duplicates(subset="id_venta")
         .dropna(subset=["unidades", "precio_unit"])
         .assign(sucursal=lambda x: x["sucursal"].str.strip().str.title())
    )
 
 
def crear_variables(d: pd.DataFrame) -> pd.DataFrame:
    return d.assign(
        importe=lambda x: (x["unidades"] * x["precio_unit"]).round(2),
        mes=lambda x: x["fecha"].dt.month,
    )
 
 
def recodificar(d: pd.DataFrame) -> pd.DataFrame:
    return d.assign(
        estatus_txt=lambda x: x["estatus"].map({1: "Pagado", 2: "Pendiente", 3: "Cancelado"}),
        grupo_edad=lambda x: pd.cut(x["edad_cliente"], [17, 30, 45, 60, 100],
                                    labels=["18-30", "31-45", "46-60", "60+"]),
        nivel_venta=lambda x: np.select(
            [x["importe"] >= 2000, x["importe"] >= 800], ["Alta", "Media"], default="Baja"
        ),
    )
 
 
def filtrar_validas(d: pd.DataFrame, min_importe: float = 100) -> pd.DataFrame:
    return d.query("estatus != 3 and importe >= @min_importe")
 
 
def resumir(d: pd.DataFrame) -> pd.DataFrame:
    return (
        d.groupby(["sucursal", "nivel_venta"], as_index=False)
         .agg(n_ventas=("id_venta", "count"),
              total=("importe", "sum"),
              ticket_prom=("importe", "mean"))
         .round(2)
         .sort_values(["sucursal", "total"], ascending=[True, False])
    )

# Principios de gráficos 

## Construir serie mensual de ventas

df = (
    cargar("Datos\\datos.csv")
    .pipe(limpiar)
    .pipe(crear_variables)
    .pipe(recodificar)
    .pipe(filtrar_validas, min_importe=100)
)

serie_mensual = df.groupby("mes")["importe"].sum()
serie_mensual

### Gráfico lineal de ventas

plt.figure(figsize=(12,7), dpi = 500)
plt.plot(serie_mensual.index, serie_mensual.values, marker = "o")
plt.title("Importe total de ventas por mes")
plt.xlabel("Mes")
plt.ylabel("Importe ($)")
plt.grid(alpha = 0.3)
plt.show()

## Gráfico de barras 

total_sucursal = df.groupby("sucursal")["importe"].sum().sort_values(ascending = False)
total_sucursal

plt.figure(figsize=(12,7), dpi = 500)
plt.bar(total_sucursal.index, total_sucursal.values, color = "steelblue")
plt.title("Total de ventas por sucursal en el año")
plt.xlabel("Sucursal")
plt.ylabel("Importe ($)")
plt.show()

## Gráfico de barras agrupadas 

tabla = df.pivot_table(index = "sucursal", columns = "categoria", values = "importe",
                       aggfunc = "sum").fillna(0)

tabla

x = np.arange(len(tabla.index))
n_cats = len(tabla.columns)
ancho = 0.8/n_cats

plt.figure(figsize=(12,7), dpi = 500)
for i, cat in enumerate(tabla.columns):
    plt.bar(x + i * ancho, tabla[cat], width = ancho, label = cat)
plt.xticks(x + ancho *(n_cats +1)/2, tabla.index)
plt.title("Total vendido por categoria y sucursal")
plt.xlabel("Sucursal")
plt.ylabel("Importe ($)")
plt.legend(title = "Categoría")
plt.show()

## Gráfico de dispersión 

plt.figure(figsize=(12,7), dpi = 500)
for cat, grupo in df.groupby("categoria"):
    plt.scatter(grupo["unidades"], grupo["importe"], label = cat, alpha = 0.8)
plt.title("Unidades vs importe por categoría")
plt.ylabel("Importe ($)")
plt.xlabel("Unidades vendidas")
plt.legend(title = "Categoría")
plt.show()


# Tipos de datos en econometría 

## Espaciales 

### Mapas de shapefile 

mexico_ent = gpd.read_file("Datos\\Mexico_ent\\00ent.shp")

mexico_ent

mexico_ent.columns

### Descripción del mapa 

print(mexico_ent.head())
print(mexico_ent.crs)
print(mexico_ent.geometry)

### Datos espaciales (sin geometría)

pobreza = pd.read_csv("Datos\\Pobreza_rel_2024.csv")

pobreza.columns

pobreza["CVE_ENT"] = pobreza["CVE_ENT"].apply(lambda m: f"{m:02d}")

## Unión de los datos con el mapa 

mexico_ent = mexico_ent.merge(
    pobreza[["CVE_ENT", "Pobreza "]],
    left_on= "CVE_ENT",
    right_on= "CVE_ENT",
    how = "left"
    )

mexico_ent


# Datos de series de tiempo 

RLM_ST = pd.read_excel("Datos\\RLM_Series_tiempo.xlsx")
RLM_ST2 = pd.read_csv("Datos\\RLM_Series_tiempo.csv")

## Revisar tipos de datos 

RLM_ST.dtypes
RLM_ST2.dtypes

## ¿Cómo transformar las fechas cuando están en str? 

texto = "01/01/2005"
fecha = datetime.strptime(texto, "%d/%m/%Y")
print(fecha)
print(texto)

RLM_ST2["Fecha"] = pd.to_datetime(RLM_ST2["Fecha"], format = "%d/%m/%Y")

# Datos de panel 

Panel_Data = pd.read_csv("Datos\\PanelData.csv")

## Crear dataframe con doble indexación 

Panel_Data2 = Panel_Data.set_index(["I", "T"])

## Verificar si es balanceado o no 

conteo = Panel_Data.groupby(["I"]).size()

conteo.nunique() == 1
print("¿Es balanceado?", conteo.nunique() == 1)

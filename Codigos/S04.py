# -*- coding: utf-8 -*-
"""
Taller: Introducción a Python 
Tema: Creación de variables, recodificació, operaciones agrupadas,
      operadores pipeline y principios de gráficos
Sesión: 04
Fecha: 18/09/2026
Docente: Alexis Adonai Morales Alberto
"""

# Instalación de modulos (ejecutar en caso de no tener el modulo)

pip install numpy pandas matplotlib

# Modulo a importar/cargar 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Lectura de datos CSV

## Método 1: Designando ruta 

# NOTA: Si la ruta contiene \ debes reemplazar por /

ruta = "E:/Econometrics Data Lab/Talleres/Introducción a Python/Datos/Homicidios_dolosos_nac_2015_2024.csv"

Hom_t = pd.read_csv(ruta)

## Método 2: Mediante espacio de trabajo del proyecto

# NOTA: Para leer un archivo desde el directorio de trabajo
# al ejecutar Python, debemos poner dentro del argumento
# de pd.read_csv comillas dobles, en medio de las comillas
# dobles se deberá presionar tab y mostrará que archivos
# se contienen en la ruta de trabajo.

Hom_t2 = pd.read_csv(
    "Datos\\Homicidios_dolosos_nac_2015_2024.csv"
    )

## Método 3: Mediante enlace web 

# NOTA: Para leer un archivo csv o txt desde una web
# el archivo debe ser público. Ejemplos más comunes son
# csv's o txt's provinientes de repositorios públicos
# de GitHub 

Hom_t3 = pd.read_csv(
    "https://raw.githubusercontent.com/econometricsdatalab-dev/Taller_INTOPY_SEP26/refs/heads/main/Datos/Homicidios_dolosos_nac_2015_2024.csv"
    )


# Lectura de archivos de excel 

# NOTA: Para leer archivo de excel (xlsx), en pandas se necesita
# un modulo que no se integra como complemento directo, se requiere
# instalarlo por separado. El modulo se llama openpyxl

pip install openpyxl

## Método 2: Mediante espacio de trabajo del proyecto

IPC_ESP = pd.read_excel(
    "Datos\\IPC_ESPAÑA.xlsx"
    )

# Simulación de datos para operaciones con datos 

rng = np.random.default_rng(42)

n = 200
datos = pd.DataFrame({
    "id_venta": range(1, n + 1),
    "fecha": pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
    "sucursal": rng.choice(["Norte", "Sur", "Centro"], n),
    "vendedor": rng.choice(["Ana", "Luis", "Marta", "Pedro"], n),
    "categoria": rng.choice(["A", "B", "C"], n),
    "unidades": rng.integers(1, 20, n),
    "precio_unit": rng.normal(150, 40, n).round(2),
    "edad_cliente": rng.integers(18, 75, n),
    "estatus": rng.choice([1, 2, 3], n),  # 1=pagado, 2=pendiente, 3=cancelado
})

datos.to_csv("Datos\\datos.csv")

# Filtros 

## De una condición 

### Valores iguales a o exactos 

df = datos[datos["sucursal"] == "Norte"]
df = datos.query(
    "sucursal == 'Sur'"
    )

### Valores mayores o menores que

df = datos[datos["edad_cliente"]>20]
df = datos[datos["edad_cliente"]<20]

df = datos.query(
    "edad_cliente > 20"
    )

df = datos.query(
    "edad_cliente < 20"
    )

### Valores mayores o igual/menores o igual

df = datos[datos["edad_cliente"]>=20]
df = datos[datos["edad_cliente"]<=20]

df = datos.query(
    "edad_cliente >= 20"
    )

df = datos.query(
    "edad_cliente <= 20"
    )

## De dos condiciones 

### Y &

df = datos[(datos["edad_cliente"]>=20) & (datos["sucursal"] == "Norte")]

df = datos.query(
    "edad_cliente >= 20 and sucursal == 'Norte'"
    )

### o |

df = datos[(datos["edad_cliente"]<=35) | (datos["sucursal"] == "Norte")]

df = datos.query(
    "edad_cliente <=35 or sucursal == 'Norte'"
    )

### NO ~

df = datos[~(datos["sucursal"] == "Norte")]
df = datos.query(
    "not (sucursal == 'Norte')"
    )

# Creación de variables 

## Método base de variable por variable

datos["importe"] = datos["unidades"] * datos["precio_unit"]

## Método usando atributo assign de pandas 

datos = datos.assign(
    mes = lambda d: d["fecha"].dt.month,
    anio = lambda d: d["fecha"].dt.year,
    importe_iva = lambda d: (d["importe"]*1.16).round(2),
    iva = lambda d: (d["importe"]*0.16).round(2)
    )

# Recodificación

## a) Método map: códigos - etiquetas (diccionario)

mapa_estatus = {1: "Pagado", 2: "Pendiente", 3: "Cancelado"}
datos["estatus_txt"] = datos["estatus"].map(mapa_estatus)

## b) Método replace: Sustituir valores puntuales 

datos["categoria_txt"] = datos["categoria"].replace(
    {
     "A": "Premium",
     "B": "Estándar",
     "C": "Básica"
     }
)

## C) Método cut: Para realizar rangos basado en una variable (numérica)

datos["edad_cliente"].min()
datos["edad_cliente"].max()

datos["grupo_edad"] = pd.cut(
    datos["edad_cliente"],
    bins = [17, 30, 45, 60, 100],
    labels = ["18-30", "31-45", "46-60", "60+"]
    )

## D) Método qcut: Cuartiles (misno número de casos por grupo)

datos["cuartil_importe"] = pd.qcut(
    datos["importe"],
    q = 4,
    labels = ["Q1", "Q2", "Q3", "Q4"]
    )

# Selección de variables de interés 

datos.columns.to_list()

Orden_var = ['id_venta',
 'fecha',
 'mes',
 'anio',
 'sucursal',
 'vendedor',
 'categoria',
 'categoria_txt',
 'unidades',
 'precio_unit',
 'importe',
 'importe_iva', 
 'iva',
 'cuartil_importe',
 'edad_cliente',
 'grupo_edad',
 'estatus',
 'estatus_txt']

datos = datos[Orden_var]

# Operaciones agrupadas 

resumen = (
    datos[datos["estatus_txt"] == "Pagado"]
    .groupby(["sucursal", "categoria_txt"])
    .agg(
        n_ventas = ("id_venta", "count"),
        total = ("importe", "sum"),
        ticket_promedio = ("importe", "mean"),
        unidades = ("unidades", "sum")
        )
    .round(2)
    .reset_index()
    .sort_values("total", ascending = False)
    )

resumen

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
 
  
reporte = (
    cargar("Datos\\datos.csv")
    .pipe(limpiar)
    .pipe(crear_variables)
    .pipe(recodificar)
    .pipe(filtrar_validas, min_importe=200)
    .pipe(resumir)
)
 
print(reporte.to_string(index=False))
 
reporte.to_csv("Datos/reporte_final.csv", index=False)


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






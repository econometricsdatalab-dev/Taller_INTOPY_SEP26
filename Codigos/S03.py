# -*- coding: utf-8 -*-
"""
Taller: Introducción a Python 
Tema: Lectura de datos y operaciones
Sesión: 03
Fecha: 17/09/2026
Docente: Alexis Adonai Morales Alberto
"""

# Instalación de modulos (ejecutar en caso de no tener el modulo)

pip install numpy pandas

# Modulo a importar/cargar 

import numpy as np
import pandas as pd

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


# Tarea 

datos_empleados = pd.DataFrame({
    "id_empleado": range(1, n + 1),
    "departamento": rng.choice(["Ventas", "IT", "Marketing", "Operaciones"], n),
    "antiguedad_anios": rng.integers(0, 15, n),
    "salario": rng.normal(45000, 12000, n).round(2),
    "horas_extras_mes": rng.integers(0, 35, n),
    "evaluacion_desempeno": rng.choice([1, 2, 3, 4, 5], n, p=[0.1, 0.2, 0.4, 0.2, 0.1]),
    "nivel_satisfaccion": rng.uniform(1.0, 10.0, n).round(1),
    "activo": rng.choice([True, False], n, p=[0.85, 0.15]),
})
from pathlib import Path
from tkinter import filedialog
import pandas as pd
import numpy as np


def renombrar_columnas(df_limpio):
    df_limpio.columns = ['Fecha_Hora', 'Potencia_Real', 'Velocidad_Viento', 'Potencia_Teorica', 'Direccion_Viento']
    return df_limpio


def convertir_tipos_datos(df_limpio):
    # Acá pones lo de pd.to_datetime, errores y ordenar por fecha
    df_limpio['Fecha_Hora']=pd.to_datetime(df_limpio['Fecha_Hora'],format='%d %m %Y %H:%M', errors='coerce')
    df_limpio=df_limpio.sort_values('Fecha_Hora')
    columnas_numericas = [
        'Potencia_Real',
        'Velocidad_Viento',
        'Potencia_Teorica',
        'Direccion_Viento',
    ]
    for col in columnas_numericas:
        if col in df_limpio.columns:
            df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')

    return df_limpio


def corregir_anomalias_fisicas(df_limpio):
    if 'Potencia_Real' in df_limpio.columns:
        df_limpio['Potencia_Real']=df_limpio['Potencia_Real'].clip(lower=0)

    return df_limpio


def eliminar_inconsistencias(df_limpio):
    df_limpio=df_limpio.dropna(subset=['Fecha_Hora'])
    df_limpio=df_limpio.drop_duplicates()
    df_limpio=df_limpio.dropna(how='all')
    return df_limpio

def calcular_eficiencia(df_limpio):
    if ('Potencia_Real' in df_limpio.columns and 'Potencia_Teorica' in df_limpio.columns):

        df_limpio['Eficiencia'] = (df_limpio['Potencia_Real'] / df_limpio['Potencia_Teorica']) * 100
        df_limpio['Eficiencia'] = df_limpio['Eficiencia'].replace([np.inf, -np.inf], np.nan).fillna(0)

    return df_limpio

def limpiar_csv(df):
    if df is None:
        return None, "No hay datos para limpiar."
    if df.shape[1]!= 5:
        return None, "El archivo no tiene el formato esperado."
    
    filas_iniciales = len(df)
    df_limpio = df.copy()
   
    df_limpio = renombrar_columnas(df_limpio)
    df_limpio = convertir_tipos_datos(df_limpio)
    df_limpio= corregir_anomalias_fisicas(df_limpio)
    df_limpio=eliminar_inconsistencias(df_limpio)
    df_limpio=calcular_eficiencia(df_limpio)
   
    filas_eliminadas = filas_iniciales - len(df_limpio)
    mensaje = (
        f"Limpieza completada. Se eliminaron {filas_eliminadas} filas."
    )

    return df_limpio, mensaje




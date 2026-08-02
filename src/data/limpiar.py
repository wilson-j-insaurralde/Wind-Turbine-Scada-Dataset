from pathlib import Path
from tkinter import filedialog
import pandas as pd


def limpiar_csv(df):
    if df is None:
        return None, "No hay datos para limpiar."

    df_limpio = df.copy()

    # Lógica de limpieza
    filas_iniciales = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates()
    df_limpio = df_limpio.dropna(how="all")

    filas_eliminadas = filas_iniciales - len(df_limpio)
    mensaje = (
        f"Limpieza completada. Se eliminaron {filas_eliminadas} filas."
    )

    return df_limpio, mensaje
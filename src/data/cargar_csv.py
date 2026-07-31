from pathlib import Path
from tkinter import filedialog
import pandas as pd


def seleccionar_y_cargar_csv():
    # 1. Abre la ventanita de Windows para elegir el archivo .csv
    ruta_seleccionada = filedialog.askopenfilename(
        title="Seleccionar Dataset SCADA",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
    )

    # Si cerrás la ventana sin elegir nada
    if not ruta_seleccionada:
        return None, "No se seleccionó ningún archivo."

    try:
        # 2. Leemos el archivo con Pandas
        ruta = Path(ruta_seleccionada)
        df = pd.read_csv(ruta)
        return df, f"Archivo '{ruta.name}' cargado con éxito."

    except Exception as e:
        return None, f"Error al leer el archivo: {str(e)}"
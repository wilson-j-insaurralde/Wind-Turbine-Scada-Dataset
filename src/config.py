from pathlib import Path

# Carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
# Carpetas de datos
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DATABASE_DIR = DATA_DIR / "database"

# Dashboard
DASHBOARD_DIR = BASE_DIR / "dashboard"
IMAGES_DIR = DASHBOARD_DIR / "images"

# Notebooks
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Archivos específicos de datos
RAW_CSV_PATH = RAW_DIR / "T1.csv"
PROCESSED_CSV_PATH = PROCESSED_DIR / "datos_turbina_procesados.csv"

#print("--- VERIFICACIÓN DE RUTAS ---")
#print("1. Raíz del proyecto:", BASE_DIR)
#print("2. Archivo CSV a buscar:", RAW_CSV_PATH)
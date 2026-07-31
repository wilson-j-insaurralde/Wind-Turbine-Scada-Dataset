from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk
from src.data.cargar_csv import seleccionar_y_cargar_csv

# Conectamos con la raíz para importar config.py
RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(RAIZ))

from src.config import APP_GEOMETRY, APP_TITLE

class VentanaPrincipal:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        # --- BARRA DE ESTADO (PIE DE PÁGINA) ---
        self.barra_estado = ttk.Label(
            self.root,
            text="Desarrollador: Wilson-J-Insaurralde",
            font=("Arial", 9, "italic"),
            relief="groove",
            anchor="e",
            padding=5,
        )
        self.barra_estado.pack(side="bottom", fill="x")

        # --- PANEL LATERAL (IZQUIERDA) ---
        self.panel_lateral = ttk.Frame(self.root, padding=10)
        self.panel_lateral.pack(side="left", fill="y")

        # Título 
        ttk.Label(
            self.panel_lateral, text="Panel de Control", font=("Arial", 12, "bold")
        ).pack(pady=10)
# --- BOTONES DEL PANEL DE CONTROL ---

        # 1. Cargar CSV
        self.btn_cargar = tk.Button(
            self.panel_lateral,
            text="📂 Abrir CSV",
            command=self.accion_cargar,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_cargar.pack(pady=5, fill="x")

        # 2. Limpiar Datos
        self.btn_limpiar = tk.Button(
            self.panel_lateral,
            text="🧹 Limpiar Datos",
            command=self.accion_limpiar,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_limpiar.pack(pady=5, fill="x")

        # 3. Estadísticas
        self.btn_estadisticas = tk.Button(
            self.panel_lateral,
            text="📊 Estadísticas",
            command=self.accion_estadisticas,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_estadisticas.pack(pady=5, fill="x")

        # 4. Gráficos
        self.btn_graficos = tk.Button(
            self.panel_lateral,
            text="📈 Gráficos",
            command=self.accion_graficos,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_graficos.pack(pady=5, fill="x")

        # 5. Exportar CSV
        self.btn_exportar_csv = tk.Button(
           self.panel_lateral,
            text="💾 Exportar CSV",
            command=self.accion_exportar_csv,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_exportar_csv.pack(pady=5, fill="x")

        # 6. Exportar PDF
        self.btn_exportar_pdf = tk.Button(
            self.panel_lateral,
            text="📄 Exportar PDF",
            command=self.accion_exportar_pdf,
            width=18,
            anchor="w",
            padx=10,
        )
        self.btn_exportar_pdf.pack(pady=5, fill="x")

        # --- ÁREA PRINCIPAL (DERECHA) ---
        self.area_principal = ttk.Frame(self.root, padding=10, relief="sunken")
        self.area_principal.pack(
            side="right", fill="both", expand=True, padx=5, pady=5
        )

        self.lbl_estado = ttk.Label(
            self.area_principal,
            text="Bienvenido. Hacé clic en 'Cargar CSV' para empezar.",
            font=("Arial", 11),
        )
        self.lbl_estado.pack(pady=20)

    # --- ACCIONES TEMPORALES PARA PROBAR ---
    def accion_cargar(self):
        # Llamamos a la función que armamos recién en cargar_csv.py
        df, mensaje = seleccionar_y_cargar_csv()

        if df is not None:
            self.df_actual = df  # Guardamos el DataFrame en la ventana
            # Mostramos en la pantalla el mensaje con la cantidad de filas y columnas
            self.lbl_estado.config(
                text=f"✅ {mensaje} | Filas: {len(df)} | Columnas: {len(df.columns)}"
            )
        else:
            self.lbl_estado.config(text=f"⚠️ {mensaje}")

    def accion_limpiar(self):
        self.lbl_estado.config(
            text="Botón Limpiar Datos presionado"
        )
    def accion_estadisticas(self):
        self.lbl_estado.config(
                    text="Botón Estadísticas presionado"
                )

    def accion_graficos(self):
        self.lbl_estado.config(
            text="Botón Gráficos presionado"
        )
    def accion_exportar_csv(self):
            self.lbl_estado.config(
                    text="Botón Exportar CSV presionado"
                )
    def accion_exportar_pdf(self):
       self.lbl_estado.config(
                   text="Botón Exportar PDF presionado"
               )
# Para poder ejecutar y probar la ventana
#if __name__ == "__main__":
#   root = tk.Tk()
#   app = VentanaPrincipal(root)
#   root.mainloop()
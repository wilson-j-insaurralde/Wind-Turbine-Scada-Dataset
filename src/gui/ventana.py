from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk

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

        # BOTÓN 1: Cargar CSV
        self.btn_cargar = ttk.Button(
            self.panel_lateral, text="📂 Cargar CSV", command=self.accion_cargar
        )
        self.btn_cargar.pack(fill="x", pady=5)

        # BOTÓN 2: Limpiar Datos
        self.btn_limpiar = ttk.Button(
            self.panel_lateral,
            text="🧹 Limpiar Datos",
            command=self.accion_limpiar,
        )
        self.btn_limpiar.pack(fill="x", pady=5)

        # BOTÓN 3: Ver Gráficos
        self.btn_graficos = ttk.Button(
            self.panel_lateral,
            text="📊 Ver Gráficos",
            command=self.accion_graficos,
        )
        self.btn_graficos.pack(fill="x", pady=5)

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
        self.lbl_estado.config(
            text="[Botón 1]: Próximamente conectamos la lectura del CSV."
        )

    def accion_limpiar(self):
        self.lbl_estado.config(
            text="[Botón 2]: Próximamente conectamos la limpieza de datos."
        )

    def accion_graficos(self):
        self.lbl_estado.config(
            text="[Botón 3]: Próximamente conectamos las gráficas."
        )

# Para poder ejecutar y probar la ventana
#if __name__ == "__main__":
#   root = tk.Tk()
#   app = VentanaPrincipal(root)
#   root.mainloop()
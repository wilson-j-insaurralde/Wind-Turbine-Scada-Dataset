from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk
from src.data.cargar_csv import seleccionar_y_cargar_csv
from src.data.limpiar import limpiar_csv
from src.analysis.estadisticas import calcular_resumen_estadistico

# Conectamos con la raíz para importar config.py
RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(RAIZ))

from src.config import APP_GEOMETRY, APP_TITLE


class VentanaPrincipal:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.df_actual = None

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
            text="Bienvenido. Hacé clic en 'Abrir CSV' para empezar.",
            font=("Arial", 11),
        )
        self.lbl_estado.pack(pady=20)

    def mostrar_tabla(self, df):
        """Limpia el área principal y dibuja una tabla (Treeview) con los datos del DataFrame."""
        # 1. Limpiamos cualquier etiqueta o tabla vieja del área blanca
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        # 2. Creamos un marco para la tabla y sus barras de desplazamiento (scroll)
        frame_tabla = ttk.Frame(self.area_principal)
        frame_tabla.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        # 3. Creamos el componente Treeview
        tabla = ttk.Treeview(
            frame_tabla,
            columns=list(df.columns),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        scroll_y.config(command=tabla.yview)
        scroll_x.config(command=tabla.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tabla.pack(fill="both", expand=True)

        # 4. Ponemos los nombres de las columnas
        for col in df.columns:
            tabla.heading(col, text=col)
            tabla.column(col, width=120, anchor="center")

        # 5. Cargar las primeras 100 filas del dataset
        for _, fila in df.head(100).iterrows():
            tabla.insert("", "end", values=list(fila))

    # --- ACCIONES ---
    def accion_cargar(self):
        # Llamamos a la función que armamos en cargar_csv.py
        df, mensaje = seleccionar_y_cargar_csv()

        if df is not None:
            self.df_actual = df  # Guardamos el DataFrame en la ventana
            # Actualizamos la barra de estado de abajo
            self.barra_estado.config(
                text=f"✅ {mensaje} | Filas: {len(df)} | Columnas: {len(df.columns)}"
            )
            # Dibujamos la tabla en la pantalla principal
            self.mostrar_tabla(df)
        else:
            self.barra_estado.config(text=f"⚠️ {mensaje}")

    def accion_limpiar(self):
        # 1. Validamos que haya un DataFrame cargado
        if self.df_actual is None:
            self.barra_estado.config(text="⚠️ Primero debes cargar un archivo CSV.")
            return

        # 2. Llamamos a limpiar_csv pasándole self.df_actual como argumento
        df_limpio, mensaje = limpiar_csv(self.df_actual)

        # 3. Guardamos el resultado de vuelta en self.df_actual (sin usar 'self.df_limpio')
        if df_limpio is not None:
            self.df_actual = df_limpio
            self.mostrar_tabla(self.df_actual)
            self.barra_estado.config(text=f"✨ {mensaje}")
       

    def accion_estadisticas(self):
        if self.df_actual is None or self.df_actual.empty:
           self.lbl_estado.config(text="Atención: Primero tenés que cargar/limpiar un archivo CSV.")
           return
    
        mensaje = calcular_resumen_estadistico(self.df_actual)

        self.lbl_estado.config(text=mensaje)

    def accion_graficos(self):
        self.lbl_estado.config(text="Botón Gráficos presionado")

    def accion_exportar_csv(self):
        self.lbl_estado.config(text="Botón Exportar CSV presionado")

    def accion_exportar_pdf(self):
        self.lbl_estado.config(text="Botón Exportar PDF presionado")
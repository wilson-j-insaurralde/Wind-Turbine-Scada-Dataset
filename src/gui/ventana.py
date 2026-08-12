from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk
from src.data.cargar_csv import seleccionar_y_cargar_csv
from src.data.limpiar import limpiar_csv
from src.analysis.estadisticas import calcular_resumen_estadistico
from src.gui.componentes.tabs_estadisticas import (
    aplicar_estilo_dashboard,
    construir_tab_dashboard,
    construir_tab_diario,
    construir_tab_mensual,
    construir_tab_viento,
)
from src.gui.componentes.panel_lateral import crear_panel_lateral
from src.gui.componentes.tabs_graficos import construir_tab_graficos
from src.utils.reportes import generar_pdf_scada
from tkinter import filedialog, messagebox
import os

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
        self.panel_lateral = crear_panel_lateral(self)

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
            self.df_original = df.copy() 
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
        # 1. Validamos que haya datos cargados
        if self.df_actual is None or self.df_actual.empty:
            self.barra_estado.config(
                text="⚠️ Atención: Primero tenés que cargar/limpiar un archivo CSV."
            )
            return

        # 2. Calculamos el resumen
        df_orig = getattr(self, "df_original", self.df_actual)
        resumen = calcular_resumen_estadistico(self.df_actual, df_orig)

        # 3. Limpiamos el área principal
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        # 4. Aplicamos estilo e iniciamos las Pestañas
        aplicar_estilo_dashboard()
        notebook = ttk.Notebook(self.area_principal)
        notebook.pack(fill="both", expand=True)

        # -- Pestaña 1: Dashboard Ejecutivo --
        tab1 = ttk.Frame(notebook, padding=15)
        notebook.add(tab1, text="📊 Dashboard Ejecutivo")
        construir_tab_dashboard(tab1, resumen)

        # -- Pestaña 2: Viento y Calidad --
        tab2 = ttk.Frame(notebook, padding=15)
        notebook.add(tab2, text="🌬️ Viento y Calidad de Datos")
        construir_tab_viento(tab2, resumen)

        # -- Pestaña 3: Reporte Mensual --
        tab3 = ttk.Frame(notebook, padding=10)
        notebook.add(tab3, text="🗓️ Reporte Mensual")
        construir_tab_mensual(tab3, resumen)

        # -- Pestaña 4: Generación Diaria --
        tab4 = ttk.Frame(notebook, padding=10)
        notebook.add(tab4, text="📅 Generación Diaria")
        construir_tab_diario(tab4, resumen)

        self.barra_estado.config(
            text="✅ Dashboard estadístico generado con éxito."
        )


    def accion_graficos(self):
        if self.df_actual is None or self.df_actual.empty:
            self.barra_estado.config(
                text="⚠️ Atención: Primero tenés que cargar/limpiar un archivo CSV para ver los gráficos."
            )
            return

        # Limpiamos el área principal
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        # Construimos el panel completo de 4 gráficos
        construir_tab_graficos(self.area_principal, self.df_actual)

        self.barra_estado.config(
            text="✅ Panel de gráficos de potencia, viento y eficiencia generado con éxito."
        )

    def accion_exportar_csv(self):
        # 1. Validar que tengamos datos para exportar
        if self.df_actual is None or self.df_actual.empty:
            messagebox.showwarning(
                "Atención",
                "Primero debés cargar y/o limpiar un archivo CSV para poder exportar."
            )
            self.barra_estado.config(
                text="⚠️ Atención: No hay datos cargados para exportar."
            )
            return

        # 2. Abrir cuadro de diálogo para seleccionar ubicación y nombre del archivo
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            title="Exportar Datos Limpios a CSV",
            initialfile="datos_turbina_procesados.csv"
        )

        # 3. Si el usuario seleccionó una ruta (no apretó cancelar)
        if ruta_guardado:
            try:
                # Exportamos a CSV sin guardar la columna de índice automático de pandas
                self.df_actual.to_csv(ruta_guardado, index=False)

                messagebox.showinfo(
                    "¡Éxito!",
                    f"El archivo se exportó correctamente en:\n{ruta_guardado}"
                )
                self.barra_estado.config(
                    text=f"✅ Datos exportados con éxito: {len(self.df_actual)} filas guardadas."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Ocurrió un error al intentar guardar el archivo CSV:\n{str(e)}"
                )

    def accion_exportar_pdf(self):
        # 1. Validar que haya datos cargados
        if self.df_actual is None or self.df_actual.empty:
            self.barra_estado.config(
                text="⚠️ Atención: Primero tenés que cargar/limpiar un archivo CSV."
            )
            return

        # 2. Elegir ruta para guardar el PDF
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar Reporte PDF",
        )

        if ruta_guardado:
            try:
                temp_img = "temp_grafico.png"
                
                # Guardar el panel de gráficos actual si existe en la pantalla
                import matplotlib.pyplot as plt
                if plt.get_fignums():
                    plt.savefig(temp_img, bbox_inches="tight", dpi=150)

                # 3. Calcular el resumen estadístico con TODAS tus funciones
                df_orig = getattr(self, "df_original", self.df_actual)
                resumen_completo = calcular_resumen_estadistico(self.df_actual, df_orig)

                # 4. Generar el PDF profesional pasándole el diccionario completo
                generar_pdf_scada(ruta_guardado, resumen_completo, temp_img)

                # Limpiar la imagen temporal
                if os.path.exists(temp_img):
                    os.remove(temp_img)

                messagebox.showinfo("¡Éxito!", f"El reporte PDF completo se generó con éxito en:\n{ruta_guardado}")
                self.barra_estado.config(text="✅ Reporte PDF exportado con éxito.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")
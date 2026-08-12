import tkinter as tk
from tkinter import ttk


def crear_panel_lateral(ventana):
    """Crea el panel de control a la izquierda con sus botones mapeados."""
    panel = ttk.Frame(ventana.root, padding=10)
    panel.pack(side="left", fill="y")

    # Título del Panel
    ttk.Label(
        panel, text="Panel de Control", font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Configuración de los botones: (Texto visual, Método que ejecuta)
    botones = [
        ("📂 Abrir CSV", ventana.accion_cargar),
        ("🧹 Limpiar Datos", ventana.accion_limpiar),
        ("📊 Estadísticas", ventana.accion_estadisticas),
        ("📈 Gráficos", ventana.accion_graficos),
        ("💾 Exportar CSV", ventana.accion_exportar_csv),
        ("📄 Exportar PDF", ventana.accion_exportar_pdf),
    ]

    # Usamos ttk.Button para mantener consistencia visual y de eventos
    for texto, comando in botones:
        btn = ttk.Button(
            panel,
            text=texto,
            command=comando,
            width=20,
        )
        btn.pack(pady=5, fill="x")

    return panel
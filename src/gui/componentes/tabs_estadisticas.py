import tkinter as tk
from tkinter import ttk


# =========================================================
# FUNCIONES AUXILIARES DE DISEÑO
# =========================================================
def aplicar_estilo_dashboard():
    """Aplica el tema visual 'clam' y los colores corporativos a las tablas."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#2B4C7E",
        foreground="white",
        padding=5,
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=25,
        fieldbackground="#FAFAFA",
    )
    style.map("Treeview", background=[("selected", "#4A7BB0")])


def agregar_filas_info(parent, datos_dict):
    """Crea filas de Clave: Valor prolijas dentro de un contenedor."""
    for label, val in datos_dict.items():
        f = ttk.Frame(parent)
        f.pack(fill="x", pady=3)
        ttk.Label(
            f, text=label, font=("Segoe UI", 9, "bold"), width=25
        ).pack(side="left")
        ttk.Label(f, text=str(val), font=("Segoe UI", 9)).pack(side="left")


def crear_tarjeta_kpi(parent, titulo, valor, subtitulo, color_borde):
    """Crea una tarjeta destacada (KPI) con número grande y borde de color."""
    frame = tk.Frame(
        parent,
        bg="white",
        highlightbackground=color_borde,
        highlightthickness=2,
        bd=0,
        padx=12,
        pady=10,
    )
    frame.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        frame,
        text=titulo.upper(),
        font=("Segoe UI", 8, "bold"),
        fg="#666666",
        bg="white",
    ).pack(anchor="w")
    tk.Label(
        frame,
        text=valor,
        font=("Segoe UI", 16, "bold"),
        fg="#1A252C",
        bg="white",
    ).pack(anchor="w", pady=(2, 0))
    tk.Label(
        frame, text=subtitulo, font=("Segoe UI", 8), fg="#888888", bg="white"
    ).pack(anchor="w")


# =========================================================
# CONSTRUCTORES DE LAS PESTAÑAS (VISTAS)
# =========================================================


def construir_tab_dashboard(tab, resumen):
    """Pestaña 1: Tarjetas de KPIs + Paneles de Potencia y Picos"""
    # 1. Tarjetas de arriba (KPIs)
    frame_kpis = ttk.Frame(tab)
    frame_kpis.pack(fill="x", pady=(0, 15))

    e = resumen["energia_total_mwh"]
    fc = resumen["factor_capacidad"]
    ef = resumen["eficiencia_operativa"]
    v = resumen["metricas_viento"]

    crear_tarjeta_kpi(
        frame_kpis,
        "Energía Generada",
        f"{e['energia_total_mwh']} MWh",
        f"{e['energia_total_kwh']} kWh totales",
        "#2B4C7E",
    )
    crear_tarjeta_kpi(
        frame_kpis,
        "Factor Capacidad",
        f"{fc['factor_capacidad_porcentaje']}%",
        "Rendimiento del Parque",
        "#27AE60",
    )
    crear_tarjeta_kpi(
        frame_kpis,
        "Eficiencia Operativa",
        f"{ef['eficiencia_operativa_porcentaje']}%",
        "Real vs Teórica",
        "#2980B9",
    )
    crear_tarjeta_kpi(
        frame_kpis,
        "Viento Medio",
        f"{v['viento_medio_ms']} m/s",
        f"Máx: {v['viento_maximo_ms']} m/s",
        "#E67E22",
    )

    # 2. Paneles de detalles en 2 columnas
    frame_columnas = ttk.Frame(tab)
    frame_columnas.pack(fill="both", expand=True)

    col_izq = ttk.LabelFrame(
        frame_columnas,
        text=" ⚡ Métricas de Potencia y Operatividad ",
        padding=10,
    )
    col_izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

    col_der = ttk.LabelFrame(
        frame_columnas, text=" 🏆 Picos y Eventos Destacados ", padding=10
    )
    col_der.pack(side="right", fill="both", expand=True, padx=(5, 0))

    pot = resumen["metricas_potencia"]
    ho = resumen["horas_operativas"]
    dia_pico = resumen["dia_pico_produccion"]
    hora_pico = resumen["hora_pico_generacion"]
    anom = resumen["anomalias"]
    corr = resumen["correlaciones"]

    agregar_filas_info(
        col_izq,
        {
            "Potencia Media:": f"{pot['potencia_media_kw']} kW",
            "Potencia Máxima:": f"{pot['potencia_maxima_kw']} kW",
            "Potencia Mínima:": f"{pot['potencia_minima_kw']} kW",
            "Horas Gen. > 1 MW:": f"{ho['horas_mas_1mw']} hs ({ho['porcentaje_mas_1mw']}%)",
            "Horas Sin Generación:": f"{ho['horas_sin_generacion']} hs ({ho['porcentaje_sin_generacion']}%)",
            "Correlación Viento/Pot.:": f"{corr['viento_vs_potencia_real']}",
        },
    )

    agregar_filas_info(
        col_der,
        {
            "Día de Máx Producción:": f"{dia_pico['dia']} ({dia_pico['energia_mwh']} MWh)",
            "Pico Potencia Día Récord:": f"{dia_pico['potencia_maxima_kw']} kW",
            "Hora Pico Habitual:": f"{hora_pico['hora_pico']}:00 hs ({hora_pico['potencia_media_kw']} kW prom.)",
            "Viento Sin Generar (Anomalía):": f"{anom['cantidad_viento_sin_potencia']} eventos",
            "Eventos Sobreproducción:": f"{anom['cantidad_sobreproduccion']} eventos",
        },
    )


def construir_tab_viento(tab, resumen):
    """Pestaña 2: Comportamiento del Viento y Auditoría de Datos"""
    est = resumen["estados_viento"]
    cal = resumen["calidad_datos"]
    per = resumen["periodo_analizado"]

    frame_viento = ttk.LabelFrame(
        tab, text=" 📊 Comportamiento del Viento (Horas y %)", padding=15
    )
    frame_viento.pack(fill="x", pady=(0, 15))

    agregar_filas_info(
        frame_viento,
        {
            "Horas en Calma (< 3 m/s):": f"{est['horas_calma']} hs ({est['porcentaje_calma']}%)",
            "Horas Operativas (3 a 25 m/s):": f"{est['horas_operativas']} hs ({est['porcentaje_operativo']}%)",
            "Horas Críticas (> 25 m/s):": f"{est['horas_criticas']} hs ({est['porcentaje_critico']}%)",
        },
    )

    frame_calidad = ttk.LabelFrame(
        tab, text=" 🧹 Auditoría de Calidad del Dataset ", padding=15
    )
    frame_calidad.pack(fill="x")

    agregar_filas_info(
        frame_calidad,
        {
            "Periodo Analizado:": f"Desde {per['fecha_inicio']} hasta {per['fecha_fin']} ({per['duracion']})",
            "Registros Originales:": f"{cal['total_original']} filas",
            "Registros Limpios Usados:": f"{cal['total_limpio']} filas",
            "Filas Eliminadas (Nulos/Anómalos):": f"{cal['filas_eliminadas']} filas",
            "Índice de Calidad de Datos:": f"{cal['porcentaje_calidad']}%",
        },
    )


def construir_tab_mensual(tab, resumen):
    """Pestaña 3: Tabla comparativa mes a mes"""
    columnas_m = ("mes", "mwh", "viento", "potencia")
    tabla_m = ttk.Treeview(tab, columns=columnas_m, show="headings")

    tabla_m.heading("mes", text="Mes (Año-Mes)")
    tabla_m.heading("mwh", text="Energía (MWh)")
    tabla_m.heading("viento", text="Viento Promedio (m/s)")
    tabla_m.heading("potencia", text="Potencia Promedio (kW)")

    for col in columnas_m:
        tabla_m.column(col, anchor="center", width=150)

    for mes, datos in resumen["df_resumen_mensual"].items():
        tabla_m.insert(
            "",
            "end",
            values=(
                mes,
                f"{datos['energia_mwh']} MWh",
                f"{datos['viento_medio_ms']} m/s",
                f"{datos['potencia_media_kw']} kW",
            ),
        )

    tabla_m.pack(fill="both", expand=True)


def construir_tab_diario(tab, resumen):
    """Pestaña 4: Tabla con scroll de la producción día por día"""
    scroll_d = ttk.Scrollbar(tab, orient="vertical")
    scroll_d.pack(side="right", fill="y")

    columnas_d = ("fecha", "kwh", "mwh")
    tabla_d = ttk.Treeview(
        tab,
        columns=columnas_d,
        show="headings",
        yscrollcommand=scroll_d.set,
    )
    scroll_d.config(command=tabla_d.yview)

    tabla_d.heading("fecha", text="Fecha")
    tabla_d.heading("kwh", text="Energía (kWh)")
    tabla_d.heading("mwh", text="Energía (MWh)")

    tabla_d.column("fecha", anchor="center", width=180)
    tabla_d.column("kwh", anchor="center", width=180)
    tabla_d.column("mwh", anchor="center", width=180)

    e = resumen["energia_total_mwh"]
    for fecha, kwh in e["energia_diaria"].items():
        tabla_d.insert(
            "",
            "end",
            values=(fecha, f"{kwh:,} kWh", f"{round(kwh/1000, 2)} MWh"),
        )

    tabla_d.pack(fill="both", expand=True)
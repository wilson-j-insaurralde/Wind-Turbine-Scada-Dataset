import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_pdf_scada(ruta_destino, resumen, ruta_imagen_grafico=None):
    """
    Genera un informe PDF profesional en 2 páginas perfectamente ordenadas,
    evitando cortes de gráficos o tablas entre páginas.
    """
    doc = SimpleDocTemplate(
        ruta_destino,
        pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=25
    )
    
    elementos = []
    estilos = getSampleStyleSheet()

    # --- ESTILOS ---
    estilo_titulo = ParagraphStyle(
        'TituloPDF', parent=estilos['Heading1'], fontSize=16, leading=18,
        textColor=colors.HexColor("#0F172A"), fontName='Helvetica-Bold'
    )
    estilo_sub = ParagraphStyle(
        'SubPDF', parent=estilos['Normal'], fontSize=8.5, leading=10,
        textColor=colors.HexColor("#64748B"), fontName='Helvetica-Oblique'
    )
    estilo_card_title = ParagraphStyle(
        'CardTitle', fontName='Helvetica-Bold', fontSize=6.5, leading=7.5,
        textColor=colors.HexColor("#475569"), alignment=1
    )
    estilo_card_value = ParagraphStyle(
        'CardValue', fontName='Helvetica-Bold', fontSize=11, leading=12,
        textColor=colors.HexColor("#0F172A"), alignment=1
    )
    estilo_card_sub = ParagraphStyle(
        'CardSub', fontName='Helvetica', fontSize=6, leading=7,
        textColor=colors.HexColor("#16A34A"), alignment=1
    )

    # --- EXTRAER DATOS ---
    mwh = f"{resumen['energia_total_mwh']['energia_total_mwh']:,.1f} MWh"
    pot_med = f"{resumen['metricas_potencia']['potencia_media_kw']:,.0f} kW"
    pot_max = f"{resumen['metricas_potencia']['potencia_maxima_kw']:,.0f} kW"
    viento_med = f"{resumen['metricas_viento']['viento_medio_ms']:.2f} m/s"
    fc = f"{resumen['factor_capacidad']['factor_capacidad_porcentaje']:.1f}%"
    eficiencia = f"{resumen['eficiencia_operativa']['eficiencia_operativa_porcentaje']:.1f}%"
    horas_1mw = f"{resumen['horas_operativas']['horas_mas_1mw']:,.0f} hs"
    porc_1mw = f"{resumen['horas_operativas']['porcentaje_mas_1mw']:.1f}% del tiempo"
    horas_sin = f"{resumen['horas_operativas']['horas_sin_generacion']:,.0f} hs"
    porc_sin = f"{resumen['horas_operativas']['porcentaje_sin_generacion']:.1f}% del tiempo"
    total_filas = f"{resumen['calidad_datos']['total_limpio']:,}"

    # ==========================================
    # 📌 PÁGINA 1: ENCABEZADO + CARDS + GRÁFICOS
    # ==========================================
    elementos.append(Paragraph("<b>INFORME DE ANÁLISIS ENERGÉTICO</b>", estilo_sub))
    elementos.append(Paragraph("<b>Turbina Eólica T1 — Análisis de Rendimiento</b>", estilo_titulo))
    elementos.append(Paragraph(f"Análisis completo basado en {total_filas} registros de medición SCADA.", estilo_sub))
    elementos.append(Spacer(1, 10))

    def crear_card(titulo, valor, subtexto):
        p_t = Paragraph(f"<b>{titulo.upper()}</b>", estilo_card_title)
        p_v = Paragraph(f"<b>{valor}</b>", estilo_card_value)
        p_s = Paragraph(subtexto, estilo_card_sub)
        
        t = Table([[p_t], [p_v], [p_s]], colWidths=[100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        return t

    c1 = crear_card("Energía Total", mwh, "✔ Producción Anual")
    c2 = crear_card("Potencia Media", pot_med, "Promedio Continuo")
    c3 = crear_card("Potencia Máxima", pot_max, "Pico Registrado")
    c4 = crear_card("Velocidad Viento", viento_med, "Promedio Anual")
    c5 = crear_card("Factor Capacidad", fc, "Rango 25-45%")
    
    c6 = crear_card("Eficiencia Operativa", eficiencia, "vs. Curva Teórica")
    c7 = crear_card("Horas > 1 MW", horas_1mw, porc_1mw)
    c8 = crear_card("Sin Generación", horas_sin, porc_sin)
    c9 = crear_card("Registros LDC", total_filas, "Limpios y Válidos")
    c10 = crear_card("Día Pico", resumen['dia_pico_produccion']['dia'], f"{resumen['dia_pico_produccion']['energia_mwh']} MWh")

    tabla_cards1 = Table([[c1, c2, c3, c4, c5]], colWidths=[106, 106, 106, 106, 106])
    tabla_cards2 = Table([[c6, c7, c8, c9, c10]], colWidths=[106, 106, 106, 106, 106])
    
    elementos.append(tabla_cards1)
    elementos.append(Spacer(1, 4))
    elementos.append(tabla_cards2)
    elementos.append(Spacer(1, 10))

    # Gráfico ajustado a una altura fija que entra perfecto en la Hoja 1
    if ruta_imagen_grafico and os.path.exists(ruta_imagen_grafico):
        elementos.append(Paragraph("<b>Paneles Analíticos SCADA</b>", estilos['Heading2']))
        elementos.append(Spacer(1, 4))
        # Reducimos un poco la altura (210 px) para que entre holgado en la Hoja 1
        elementos.append(Image(ruta_imagen_grafico, width=530, height=210))

    # 🛑 SALTO DE PÁGINA FORZADO
    elementos.append(PageBreak())

    # ==========================================
    # 📌 PÁGINA 2: TABLA MENSUAL + HALLAZGOS
    # ==========================================
    elementos.append(Paragraph("<b>Desglose Estadístico Mensual</b>", estilos['Heading2']))
    elementos.append(Spacer(1, 8))

    filas_tabla = [["Mes", "Energía (MWh)", "Viento Medio (m/s)", "Pot. Media (kW)"]]
    resumen_mensual = resumen.get('df_resumen_mensual', {})
    
    for mes, datos in resumen_mensual.items():
        filas_tabla.append([
            mes,
            f"{datos['energia_mwh']:,.2f}",
            f"{datos['viento_medio_ms']:.2f}",
            f"{datos['potencia_media_kw']:,.1f}"
        ])

    tabla_mensual = Table(filas_tabla, colWidths=[110, 140, 140, 140])
    tabla_mensual.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_mensual)
    elementos.append(Spacer(1, 20))

    # Sección de Conclusiones al pie de la Página 2
    elementos.append(Paragraph("<b>Conclusiones y Hallazgos Clave</b>", estilos['Heading2']))
    elementos.append(Spacer(1, 8))

    hallazgos = [
        ["<b>Mejor Periodo:</b>", f"El día con mayor generación fue <b>{resumen['dia_pico_produccion']['dia']}</b> con <b>{resumen['dia_pico_produccion']['energia_mwh']} MWh</b>."],
        ["<b>Eficiencia Operativa:</b>", f"La turbina opera al <b>{eficiencia}</b> de su curva teórica, manteniendo alta confiabilidad."],
        ["<b>Horas Operativas:</b>", f"El parque operó por encima de 1 MW el <b>{porc_1mw}</b> del tiempo total analizado."]
    ]

    tabla_hallazgos = Table(
        [[Paragraph(h[0], estilos['Normal']), Paragraph(h[1], estilos['Normal'])] for h in hallazgos],
        colWidths=[140, 390]
    )
    tabla_hallazgos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla_hallazgos)

    # Construir PDF
    doc.build(elementos)
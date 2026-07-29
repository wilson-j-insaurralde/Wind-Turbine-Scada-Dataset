# 💨 Wind Turbine SCADA Performance Analysis

Análisis de datos (ETL, EDA y Visualización) sobre más de 50.000 registros SCADA de una turbina eólica utilizando Python.

## 🛠️ Tecnologías

- Python (Pandas, NumPy, Matplotlib)
- Power BI (Próximamente)

## 📊 KPIs Principales

- Registros analizados: 50.530
- Velocidad promedio del viento: 7.56 m/s
- Potencia real promedio: 1.307.68 kW
- Potencia teórica promedio: 1.492.18 kW
- Eficiencia operativa promedio: 68.68 %

## 📈 Contenido del Proyecto

1. Limpieza y transformación de datos (ETL).
2. Conversión y procesamiento de fechas.
3. Cálculo de KPIs operativos.
4. Análisis estacional mediante `groupby`.
5. Visualización de potencia, viento y eficiencia.
6. Exportación del conjunto de datos procesado para Power BI.

## 🔍 Principales hallazgos

- La producción de energía presenta una marcada variación estacional.
- La potencia real sigue, en términos generales, la tendencia de la curva de potencia teórica.
- La mayor producción se registra durante los meses con mayor velocidad promedio del viento.

## ⚠️ Limitaciones del análisis

Se detectaron registros con eficiencias superiores al 100 %, principalmente a bajas velocidades del viento (≈3 m/s). Estos valores no indican que la turbina supere sus límites físicos de eficiencia, sino que probablemente estén asociados a la elevada sensibilidad de la curva de potencia en la región de arranque (*cut-in*), variaciones rápidas del viento, posibles desfases temporales entre sensores o incertidumbre en las mediciones. Por ello, estos registros deben interpretarse como casos atípicos propios de datos SCADA y no como un incremento real del rendimiento de la turbina.

---

*Proyecto de Análisis de Datos aplicado a sistemas SCADA de generación eólica.*

## 📷 Visualizaciones

### Dashboard 1

![Dashboard SCADA 1](01_dashboard_graficos.png)

### Dashboard 2

![Dashboard SCADA 2](02_dashboard_graficos.png)

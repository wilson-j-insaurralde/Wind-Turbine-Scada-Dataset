# **💨 Wind Turbine SCADA Performance Analysis**

Proyecto de Análisis de Datos y visualización utilizando información SCADA de una turbina eólica.  
El proyecto incluye el proceso completo de carga, limpieza, transformación (ETL), análisis exploratorio (EDA), cálculo de indicadores (KPIs) y una aplicación modular con interfaz gráfica (Tkinter) para la visualización de datos. Además, los datos procesados quedan preparados para su análisis en Power BI.

## ---

**📂 Estructura del Proyecto**

WIND\_TURBINE\_SCADA\_DATASET/  
├── dashboard/  
│   └── images/          \# Capturas de pantalla para el README y presentaciones  
├── data/  
│   ├── raw/             \# Archivos CSV SCADA originales (intocables)  
│   ├── processed/       \# Datos procesados (Parquet/CSV)  
│   └── database/        \# Base de datos local (SQLite)  
├── notebooks/           \# Exploración inicial (EDA) en Jupyter  
├── src/  
│   ├── main.py          \# Punto de entrada de la aplicación  
│   ├── config.py        \# Rutas dinámicas y constantes del sistema  
│   ├── gui/             \# Capa de Interfaz Gráfica (Tkinter)  
│   │   ├── \_\_init\_\_.py  
│   │   ├── ventana.py  
│   │   ├── menu.py  
│   │   ├── toolbar.py  
│   │   ├── panel.py  
│   │   ├── tablas.py  
│   │   ├── graficos.py  
│   │   └── dialogs.py  
│   ├── data/            \# Capa de Ingesta y ETL  
│   │   ├── \_\_init\_\_.py  
│   │   ├── cargar\_csv.py  
│   │   ├── limpiar.py  
│   │   └── transformar.py  
│   ├── analysis/        \# Capa de Cálculo y Análisis SCADA  
│   │   ├── \_\_init\_\_.py  
│   │   ├── estadisticas.py  
│   │   ├── correlacion.py  
│   │   └── tendencias.py  
│   └── utils/           \# Helpers, formateadores y logs  
│       ├── \_\_init\_\_.py  
│       └── helpers.py  
├── dataset\_info.txt     \# Descripción y metadatos del dataset  
├── requirements.txt     \# Dependencias del proyecto  
└── README.md

## ---

**🛠️ Tecnologías utilizadas**

> * Python  
> * Pandas  
> * NumPy  
> * Matplotlib  
> * Tkinter  
> * Jupyter Notebook  
> * Power BI (Próximamente)

## ---

**📊 Indicadores Principales (KPIs)**

| Indicador | Valor   |
| :---- | ----- |
| Registros analizados | 50.530 |
| Velocidad promedio del viento | 7.56 m/s |
| Potencia real promedio | 1.307,68 kW |
| Potencia teórica promedio | 1.492,18 kW |
| Eficiencia operativa promedio | 68,68 % |

## ---

**📈 Contenido del Proyecto**

> * Carga del conjunto de datos.  
> * Limpieza y transformación de datos (ETL).  
> * Conversión y procesamiento de fechas.  
> * Cálculo de indicadores operativos (KPIs).  
> * Análisis exploratorio de datos (EDA).  
> * Visualización de variables y tendencias mediante interfaz gráfica (Tkinter).  
> * Exportación del conjunto de datos procesado para Power BI.

## ---

**🔍 Principales hallazgos**

> * La producción de energía presenta un comportamiento estacional claramente definido.  
> * La potencia real sigue, en términos generales, la tendencia de la curva de potencia teórica.  
> * Los meses con mayor velocidad promedio del viento registran una mayor generación de energía.  
> * El conjunto de datos procesado queda preparado para su análisis mediante Power BI.

## ---

**⚠️ Limitaciones del análisis**

Se detectaron registros con eficiencias superiores al 100 %, principalmente a bajas velocidades del viento (≈3 m/s).  
Estos valores no indican que la turbina supere sus límites físicos de eficiencia. Lo más probable es que estén asociados a:

> * La elevada sensibilidad de la curva de potencia en la zona de arranque (*cut-in*).  
> * Variaciones rápidas de la velocidad del viento.  
> * Pequeños desfases temporales entre sensores SCADA.  
> * Incertidumbre propia de las mediciones.

Por ello, estos registros deben interpretarse como valores atípicos propios de este tipo de sistemas y no como un aumento real del rendimiento de la turbina.

## ---

**📷 Visualizaciones**

### **Dashboard 1**

\!\[Dashboard 1\](dashboard/images/01\_dashboard\_graficos.png)

### **Dashboard 2**

\!\[Dashboard 2\](dashboard/images/02\_dashboard\_graficos.png)

## ---

**📁 Organización de los datos**

El archivo original del dataset se encuentra en:  
data/raw/  
El archivo procesado generado durante el análisis se guarda en:  
data/processed/  
La información sobre el origen del dataset y la descripción de las variables se encuentra en:  
dataset\_info.txt

## ---

**🚀 Próximas mejoras**

> * Dashboard interactivo en Power BI.  
> * Aplicación de escritorio desarrollada con Tkinter.  
> * Automatización del procesamiento de archivos SCADA.  
> * Generación automática de reportes.  
> * Modelos de Machine Learning para predicción de potencia.  
> * Detección de anomalías.  
> * Análisis de mantenimiento predictivo.

---

**Proyecto de Ciencia de Datos y Análisis de Datos aplicado a sistemas SCADA de generación eólica.**
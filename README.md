# 💨 Wind Turbine SCADA Performance Analysis

Proyecto de Análisis de Datos y visualización utilizando información SCADA de una turbina eólica.  
El proyecto incluye el proceso completo de carga, limpieza, transformación (ETL), análisis exploratorio (EDA), cálculo de indicadores (KPIs) y una aplicación modular con interfaz gráfica (Tkinter) para la visualización de datos. Además, los datos procesados quedan preparados para su análisis en Power BI.

---

### 📂 Estructura del Proyecto

```text
WIND_TURBINE_SCADA_DATASET/  
├── data/  
│   ├── raw/             # Archivos CSV SCADA originales (T1.csv)
│   └── processed/       # Datos procesados (datos_turbina_procesados.csv)
├── notebooks/           # Análisis exploratorio (EDA)
│   └── turbina_scada_analisis.ipynb
├── src/  
│   ├── main.py          # Punto de entrada de la aplicación  
│   ├── config.py        # Rutas dinámicas y constantes del sistema  
│   ├── analysis/        # Módulos de Cálculo y Análisis SCADA  
│   │   ├── correlacion.py  
│   │   ├── estadisticas.py  
│   │   └── tendencias.py  
│   ├── data/            # Módulos de Ingesta y Limpieza  
│   │   ├── cargar_csv.py  
│   │   └── limpiar.py  
│   ├── gui/             # Interfaz Gráfica (Tkinter)  
│   │   ├── componentes/  
│   │   └── ventana.py  
│   └── utils/           # Generación de Reportes PDF y Helpers  
│       └── reportes.py  
├── dataset_info.txt     # Descripción y metadatos del dataset  
├── requirements.txt     # Dependencias del proyecto  
└── README.md 
```

---

###🛠️ Tecnologías utilizadas

> * Python  
> * Pandas  
> * NumPy  
> * Matplotlib  
> * Tkinter  
> * Jupyter Notebook
> * ReportLab (Generación de PDF)
> * Power BI (Próximamente)

---

###📊 Indicadores Principales (KPIs)

| Indicador | Valor   |
| :---- | ----- |
| Registros analizados | 50.530 |
| Velocidad promedio del viento | 7.56 m/s |
| Potencia real promedio | 1.307,68 kW |
| Potencia teórica promedio | 1.492,18 kW |
| Eficiencia operativa promedio | 68,68 % |

---

###📈 Contenido del Proyecto 

> * Carga del conjunto de datos.  
> * Limpieza y transformación de datos (ETL).  
> * Conversión y procesamiento de fechas.  
> * Cálculo de indicadores operativos (KPIs).  
> * Análisis exploratorio de datos (EDA).  
> * Visualización de variables y tendencias mediante interfaz gráfica (Tkinter).  
> * Exportación automática de reportes en PDF.
> * Exportación del conjunto de datos procesado para Power BI.

---

###🔍 Principales hallazgos 

> * La producción de energía presenta un comportamiento estacional claramente definido.  
> * La potencia real sigue, en términos generales, la tendencia de la curva de potencia teórica.  
> * Los meses con mayor velocidad promedio del viento registran una mayor generación de energía.  
> * El conjunto de datos procesado queda preparado para su análisis mediante Power BI.

---

###⚠️ Limitaciones del análisis 

Se detectaron registros con eficiencias superiores al 100 %, principalmente a bajas velocidades del viento (≈3 m/s).  
Estos valores no indican que la turbina supere sus límites físicos de eficiencia. Lo más probable es que estén asociados a:

> * La elevada sensibilidad de la curva de potencia en la zona de arranque (*cut-in*).  
> * Variaciones rápidas de la velocidad del viento.  
> * Pequeños desfases temporales entre sensores SCADA.  
> * Incertidumbre propia de las mediciones.

Por ello, estos registros deben interpretarse como valores atípicos propios de este tipo de sistemas y no como un aumento real del rendimiento de la turbina.

---

###📷 Visualizaciones 

#### 🎬 Demostración de la Aplicación
![Demo de la aplicación](turbine-tkinter-gif.gif)

### **Dashboard 1**

![Dashboard 1](dashboard/images/01_dashboard_graficos.png)

### **Dashboard 2**

![Dashboard 2](dashboard/images/02_dashboard_graficos.png)

---

###📁 Organización de los datos 

El archivo original del dataset se encuentra en:  
data/raw/  
El archivo procesado generado durante el análisis se guarda en:  
data/processed/  
La información sobre el origen del dataset y la descripción de las variables se encuentra en:  
dataset\_info.txt

---

###🚀 Próximas mejoras

> * Dashboard interactivo en Power BI.  
> * Aplicación de escritorio desarrollada con Tkinter.  
> * Automatización del procesamiento de archivos SCADA.  
> * Generación automática de reportes.  
> * Modelos de Machine Learning para predicción de potencia.  
> * Detección de anomalías.  
> * Análisis de mantenimiento predictivo.

---


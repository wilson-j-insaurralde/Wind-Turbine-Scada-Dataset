import pandas as pd
import numpy as np

def obtener_intervalo_horas(df):
    """
    Detecta automáticamente el intervalo entre mediciones
    y lo devuelve en horas.
    """
    diferencia = df['Fecha_Hora'].iloc[1] - df['Fecha_Hora'].iloc[0]

    intervalo_horas = diferencia.total_seconds() / 3600

    return intervalo_horas
def calcular_periodo_analizado(df):    
    fecha_inicio=df['Fecha_Hora'].min()
    fecha_fin=df['Fecha_Hora'].max()
    duracion= fecha_fin - fecha_inicio
    return {
        'fecha_inicio':fecha_inicio,
        'fecha_fin' : fecha_fin,
        'duracion' : duracion,
    }


def calcular_calidad_datos(df,df_original):
    total_original = len(df_original)
    total_limpio = len(df)
    filas_eliminadas=total_original-total_limpio
    porcentaje=(total_limpio/total_original)*100 if total_original>0 else 0.0
    return {
        'total_original': total_original,
        'total_limpio': total_limpio,
        'filas_eliminadas': filas_eliminadas,
        'porcentaje_calidad': round(porcentaje,2),
    }


def calcular_energia_total(df, intervalo_horas):
    energia_kwh = df['Potencia_Real'] * intervalo_horas
    total_kwh = energia_kwh.sum()
    energia_diaria = energia_kwh.groupby(df['Fecha_Hora'].dt.date.astype(str)).sum().round(2).to_dict()
    energia_mensual = energia_kwh.groupby(df['Fecha_Hora'].dt.to_period('M').astype(str)).sum().round(2).to_dict()
    
    return {
        'energia_total_kwh': round(total_kwh, 2),
        'energia_total_mwh': round(total_kwh / 1000, 2),
        'energia_diaria': energia_diaria,    # Ej: {'2026-08-01': 450.2, ...}
        'energia_mensual': energia_mensual   # Ej: {'2026-08': 12500.5, ...}
    }



def calcular_metricas_potencia(df):
    pass


def calcular_metricas_viento(df):
    pass


def calcular_factor_capacidad(df):
    pass


def calcular_eficiencia_operativa(df):
    pass


def calcular_horas_operativas(df):
    pass


def calcular_resumen_mensual(df):
    pass


def calcular_dia_mayor_produccion(df):
    pass


def calcular_estados_viento(df):
    pass


def calcular_hora_pico_generacion(df):
    pass


def calcular_correlaciones(df):
    pass


def calcular_anomalias(df):
    pass


def calcular_resumen_estadistico(df: pd.DataFrame,df_original:pd.DataFrame=None):

    obtener_intervalo = obtener_intervalo_horas(df)
    periodo_analizado = calcular_periodo_analizado(df)
    calidad_datos = calcular_calidad_datos(df,df_original)

    energia_total_mwh = calcular_energia_total(df, obtener_intervalo)
    metricas_potencia = calcular_metricas_potencia(df)
    metricas_viento = calcular_metricas_viento(df)

    factor_capacidad = calcular_factor_capacidad(df)
    eficiencia_operativa = calcular_eficiencia_operativa(df)
    horas_operativas = calcular_horas_operativas(df)

    df_resumen_mensual = calcular_resumen_mensual(df)

    dia_pico_produccion = calcular_dia_mayor_produccion(df)
    estados_viento = calcular_estados_viento(df)
    hora_pico_generacion = calcular_hora_pico_generacion(df)

    correlaciones = calcular_correlaciones(df)
    anomalias = calcular_anomalias(df)


    return {
        'periodo_analizado': periodo_analizado,
        'calidad_datos': calidad_datos,
        'energia_total_mwh':energia_total_mwh,
        

    }
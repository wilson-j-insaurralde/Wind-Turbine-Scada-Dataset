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
    potencia_media=df['Potencia_Real'].mean()
    potencia_maxima=df['Potencia_Real'].max()
    potencia_minima=df['Potencia_Real'].min()

    return {
        'potencia_media_kw':round(potencia_media,2),
        'potencia_maxima_kw':round(potencia_maxima,2),
        'potencia_minima_kw':round(potencia_minima,2),
    }


def calcular_metricas_viento(df):
    viento_medio_ms = df['Velocidad_Viento'].mean()
    viento_maximo_ms = df['Velocidad_Viento'].max()
    viento_minimo_ms = df['Velocidad_Viento'].min()
    return {
        'viento_medio_ms':round(viento_medio_ms, 2),
        'viento_maximo_ms':round(viento_maximo_ms, 2),
        'viento_minimo_ms':round(viento_minimo_ms, 2),
    }


def calcular_factor_capacidad(df):
    potencia_media = df['Potencia_Real'].mean()
    potencia_maxima = df['Potencia_Real'].max()
    if potencia_maxima>0:
        factor_capacidad=(potencia_media/potencia_maxima)*100
    else:
        factor_capacidad=0.0
    return{
        'factor_capacidad_porcentaje':round(factor_capacidad,2),
    }



def calcular_eficiencia_operativa(df):
    suma_real = df['Potencia_Real'].sum()
    suma_teorica = df['Potencia_Teorica'].sum()

    if suma_teorica >0:
        eficiencia=(suma_real/suma_teorica)*100
    else:
        eficiencia=0.0
    return {
        'eficiencia_operativa_porcentaje':round(eficiencia, 2)
    }


def calcular_horas_operativas(df,obtener_intervalo):
    # 1. Horas generando > 1 MW (1000 kW)
    filas_mas_1mw=df[df['Potencia_Real']>1000]
    horas_mas_1mw=len(filas_mas_1mw)*obtener_intervalo
    # 2. Horas sin generación (Potencia <= 0 kW)
    filas_sin_generacion=df[df['Potencia_Real']<=0]
    horas_sin_generacion=len(filas_sin_generacion)*obtener_intervalo
    # 3. Porcentajes sobre el tiempo total
    horas_totales = len(df)*obtener_intervalo
    porcentaje_mas_1mw=(horas_mas_1mw/horas_totales)*100 if horas_totales>0 else 0.0
    porcentaje_sin_generacion=(horas_sin_generacion/horas_totales)*100 if horas_totales>0 else 0.0
    return{
        'horas_mas_1mw':round(horas_mas_1mw,2),
        'porcentaje_mas_1mw':round(porcentaje_mas_1mw,2),
        'horas_sin_generacion':round(horas_sin_generacion,2),
        'porcentaje_sin_generacion':round(porcentaje_sin_generacion,2)
    }

       


def calcular_resumen_mensual(df,obtener_intervalo):
    df_temp=df.copy()
    df_temp['Mes']=df_temp['Fecha_Hora'].dt.to_period('M').astype(str)

    resumen={}
    for mes,grupo in df_temp.groupby('Mes'):
        energia_mwh = (grupo['Potencia_Real'] * obtener_intervalo).sum() / 1000
        resumen[mes] = {
            'energia_mwh': round(energia_mwh, 2),
            'viento_medio_ms': round(grupo['Velocidad_Viento'].mean(), 2),
            'potencia_media_kw': round(grupo['Potencia_Real'].mean(), 2)
        }
        
    return resumen
    


def calcular_dia_mayor_produccion(df, intervalo_horas):
    df_temp = df.copy()
    df_temp['Dia'] = df_temp['Fecha_Hora'].dt.to_period('D').astype(str)
    resumen_dias = {}
    for dia, grupo in df_temp.groupby('Dia'):
        energia_mwh = (grupo['Potencia_Real'] * intervalo_horas).sum() / 1000
        resumen_dias[dia] = {
            'energia_mwh': energia_mwh,
            'potencia_media_kw': grupo['Potencia_Real'].mean(),
            'potencia_maxima_kw': grupo['Potencia_Real'].max(),
            'viento_medio_ms': grupo['Velocidad_Viento'].mean(),
            'viento_maximo_ms': grupo['Velocidad_Viento'].max(),
            'cantidad_registros': len(grupo)
        }
    energia_maxima = 0
    dia_maximo = None
    for dia, datos in resumen_dias.items():
        if datos['energia_mwh'] > energia_maxima:
            energia_maxima = datos['energia_mwh']
            dia_maximo = dia
    datos = resumen_dias[dia_maximo]
    return {
        'dia': dia_maximo,
        'energia_mwh': round(datos['energia_mwh'], 2),
        'potencia_media_kw': round(datos['potencia_media_kw'], 2),
        'potencia_maxima_kw': round(datos['potencia_maxima_kw'], 2),
        'viento_medio_ms': round(datos['viento_medio_ms'], 2),
        'viento_maximo_ms': round(datos['viento_maximo_ms'], 2),
        'cantidad_registros': datos['cantidad_registros']
    }


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
    horas_operativas = calcular_horas_operativas(df,obtener_intervalo)

    df_resumen_mensual = calcular_resumen_mensual(df,obtener_intervalo)

    dia_pico_produccion = calcular_dia_mayor_produccion(df,obtener_intervalo)
    estados_viento = calcular_estados_viento(df)
    hora_pico_generacion = calcular_hora_pico_generacion(df)

    correlaciones = calcular_correlaciones(df)
    anomalias = calcular_anomalias(df)


    return {
        'periodo_analizado': periodo_analizado,
        'calidad_datos': calidad_datos,
        'energia_total_mwh':energia_total_mwh,
        'metricas_potencia': metricas_potencia,
        'metricas_viento': metricas_viento,
        'factor_capacidad':factor_capacidad,
        'eficiencia_operativa':eficiencia_operativa,
        'horas_operativas':horas_operativas,
        'df_resumen_mensual':df_resumen_mensual,
        'dia_pico_produccion': dia_pico_produccion,



        
    }
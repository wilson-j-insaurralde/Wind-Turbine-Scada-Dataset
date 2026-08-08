import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk

def construir_tab_graficos(parent_frame, df):
    """
    Recibe el Frame contenedor de Tkinter y el DataFrame limpio.
    Dibuja un panel de 4 gráficos esenciales para monitoreo eólico.
    """
    # Creamos la figura con 4 subplots (2 filas x 2 columnas)
    fig, axes = plt.subplots(2, 2, figsize=(11, 6), dpi=100)
    fig.patch.set_facecolor('#f4f5f7')  # Fondo gris prolijo
    (ax1, ax2), (ax3, ax4) = axes

    # --- 1. CURVA DE POTENCIA (Real vs Teórica) ---
    if 'Velocidad_Viento' in df.columns and 'Potencia_Real' in df.columns:
        ax1.scatter(df['Velocidad_Viento'], df['Potencia_Real'], alpha=0.3, color='#1f77b4', s=8, label='Real')
        
        if 'Potencia_Teorica' in df.columns:
            # Ordenamos para dibujar la curva teórica limpia como una línea
            df_ordenado = df.sort_values('Velocidad_Viento')
            ax1.plot(df_ordenado['Velocidad_Viento'], df_ordenado['Potencia_Teorica'], color='#d62728', linewidth=1.5, label='Teórica')
            
        ax1.set_title("Curva de Potencia vs. Viento", fontsize=10, fontweight='bold')
        ax1.set_xlabel("Velocidad Viento (m/s)", fontsize=8)
        ax1.set_ylabel("Potencia (kW)", fontsize=8)
        ax1.legend(loc='upper left', fontsize=8)
        ax1.grid(True, linestyle='--', alpha=0.5)

    # --- 2. DISTRIBUCIÓN DE VELOCIDAD DE VIENTO (Historigrama) ---
    if 'Velocidad_Viento' in df.columns:
        ax2.hist(df['Velocidad_Viento'].dropna(), bins=25, color='#2ca02c', edgecolor='black', alpha=0.7)
        ax2.set_title("Distribución de Velocidad de Viento", fontsize=10, fontweight='bold')
        ax2.set_xlabel("Velocidad Viento (m/s)", fontsize=8)
        ax2.set_ylabel("Frecuencia (Registros)", fontsize=8)
        ax2.grid(True, linestyle='--', alpha=0.5)

    # --- 3. RENDIMIENTO Y EFICIENCIA (%) ---
    if 'Eficiencia' in df.columns:
        # Filtramos valores atípicos extremados para que el gráfico quede bien proporcionado
        eficiencia_filtrada = df['Eficiencia'][(df['Eficiencia'] >= 0) & (df['Eficiencia'] <= 150)]
        ax3.hist(eficiencia_filtrada, bins=20, color='#ff7f0e', edgecolor='black', alpha=0.7)
        ax3.set_title("Distribución de Eficiencia Operativa (%)", fontsize=10, fontweight='bold')
        ax3.set_xlabel("Eficiencia (%)", fontsize=8)
        ax3.set_ylabel("Frecuencia", fontsize=8)
        ax3.grid(True, linestyle='--', alpha=0.5)

    # --- 4. DIRECCIÓN DEL VIENTO VS POTENCIA ---
    if 'Direccion_Viento' in df.columns and 'Potencia_Real' in df.columns:
        ax4.scatter(df['Direccion_Viento'], df['Potencia_Real'], alpha=0.3, color='#9467bd', s=8)
        ax4.set_title("Dirección del Viento (°) vs. Potencia (kW)", fontsize=10, fontweight='bold')
        ax4.set_xlabel("Dirección del Viento (Grados °)", fontsize=8)
        ax4.set_ylabel("Potencia Real (kW)", fontsize=8)
        ax4.set_xlim(0, 360)
        ax4.grid(True, linestyle='--', alpha=0.5)

    # Ajustamos márgenes para que no se encimen los textos
    fig.tight_layout()

    # Incrustamos la figura dentro de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
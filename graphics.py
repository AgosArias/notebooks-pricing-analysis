import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import logging

logging.basicConfig(level=logging.INFO)

def grafico_dispersion_precios(df):
    """
    Crea un gráfico de dispersión de precios de productos.
    
    Args:
        df (DataFrame): El DataFrame que contiene los datos a graficar.
    """
    if df is not None and not df.empty:
        plt.figure(figsize=(12, 8))
        plt.scatter(df['Marca'], df['Precio'], alpha=0.7, color='pink', edgecolor='k', s=100)
        plt.xticks(rotation=90)
        plt.xlabel('Marca', fontsize=12)
        plt.ylabel('Precio', fontsize=12)
        plt.title('Precios de Productos Electrónicos', fontsize=16)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_etiquetas))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        logging.warning("El DataFrame está vacío o es None.")

def formatear_etiquetas(x, pos):
    """
    Formatea las etiquetas del eje y para mostrar en miles (K) o millones (M).
    
    Args:
        x (float): Valor del eje.
        pos (int): Posición del eje.
    
    Returns:
        str: Valor formateado.
    """
    if x >= 1000000:
        return f'{int(x/1000000)}M'
    elif x >= 1000:
        return f'{int(x/1000)}K'
    else:
        return int(x)

def grafico_histogramas_por_marca(df):
    """
    Crea histogramas de la distribución de precios para cada marca.
    
    Args:
        df (DataFrame): El DataFrame que contiene los datos a graficar.
    """
    if df is not None and not df.empty:
        marcas = df['Marca'].unique()  # Obtener las marcas únicas
        for marca in marcas:
            # Filtrar precios mayores o iguales a 10,000
            df_filtrado = df[df['Precio'] >= 10000]
            
            plt.figure(figsize=(12, 8))
            plt.hist(df_filtrado['Precio'], bins=30, color='skyblue', edgecolor='black')
            plt.xlabel('Precio', fontsize=12)
            plt.ylabel('Frecuencia', fontsize=12)
            plt.title(f'Distribución de Precios de Notebooks de {marca}', fontsize=16)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(formatear_etiquetas))
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    else:
        logging.warning("El DataFrame está vacío o es None.")

def grafico_boxplot(df):
    """
    Crea un boxplot de precios por marca.
    
    Args:
        df (DataFrame): El DataFrame que contiene los datos a graficar.
    """
    if df is not None and not df.empty:
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Marca', y='Precio', data=df, palette='Set2')
        plt.xlabel('Marca', fontsize=12)
        plt.ylabel('Precio', fontsize=12)
        plt.title('Distribución de Precios por Marca', fontsize=16)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_etiquetas))
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        logging.warning("El DataFrame está vacío o es None.")

def grafico_barras_marca(df):
    """
    Crea un gráfico de barras mostrando el número de productos por marca.
    
    Args:
        df (DataFrame): El DataFrame que contiene los datos a graficar.
    """
    if df is not None and not df.empty:
        categoria_counts = df['Marca'].value_counts()
        plt.figure(figsize=(10, 6))
        categoria_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.xlabel('Marca', fontsize=12)
        plt.ylabel('Número de Productos', fontsize=12)
        plt.title('Número de Productos por Marca', fontsize=16)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        logging.warning("El DataFrame está vacío o es None.")

def normalize_data(df):
    """
    Normaliza el DataFrame eliminando duplicados, filtrando marcas frecuentes,
    y ordenando los datos por precio.
    
    Args:
        df (DataFrame): El DataFrame que contiene los datos a normalizar.
    
    Returns:
        DataFrame: El DataFrame normalizado.
    """
    if df is not None and not df.empty:
        # Eliminar duplicados
        df = df.drop_duplicates()
        
        # Filtrar marcas con más de 3 productos
        conteo_marcas = df['Marca'].value_counts()
        marcas_frecuentes = conteo_marcas[conteo_marcas > 3].index
        df = df[df['Marca'].isin(marcas_frecuentes)]
        
        # Convertir la columna 'Precio' a numérico
        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
        
        # Eliminar valores NaN en la columna 'Precio'
        df = df.dropna(subset=['Precio'])
        
        # Eliminar los datos con precio menor a 100,000
        df = df[df['Precio'] >= 100000]
        
        # Ordenar el DataFrame por la columna 'Precio'
        df = df.sort_values(by='Precio')
        
        return df
    else:
        logging.warning("El DataFrame está vacío o es None.")
        return pd.DataFrame()  # Retornar un DataFrame vacío si la entrada es inválida

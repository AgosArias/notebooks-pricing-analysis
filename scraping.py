import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# Lista de marcas populares de notebooks
marcas_populares = [
    'HP', 'ACER', 'DELL', 'APPLE', 'LENOVO', 'ASUS', 'MICROSOFT', 
    'SAMSUNG', 'MSI', 'TOSHIBA', 'NSX', 'ALIENWARE', 'AORUS', 
    'BANGHÓ', 'BGH', 'CHUWI', 'COMMODORE', 'COMPAQ', 'CORADIR', 
    'CX', 'DAEWOO', 'DYNABOOK', 'EMACHINES', 'ENOVA', 'EUROCASE', 
    'EVOO', 'EXO', 'GATEWAY', 'GENÉRICA', 'GFAST', 'GIGABYTE', 
    'GPD', 'HITACHI', 'HUAWEI', 'HYPERX', 'HYUNDAI', 'iQUAL', 
    'KAIROS', 'KANJI', 'KELYX', 'KEN BROWN', 'LG', 'MAC', 'MACBOOK', 
    'NETSYS', 'NOBLEX', 'OLIVETTI', 'PACKARD BELL', 'PCBOX', 
    'PHILCO', 'POSITIVO', 'POSITIVO BGH', 'RAZER', 'RCA', 
    'RICILAR', 'SONY', 'SOPHO', 'TEDGE', 'VAIO', 'VENTURER', 
    'VIEWSONIC', 'X-VIEW', 'XPG'
]

def modelar_datos_pagina(url, nombres, precios, marcas, urls):
    """
    Función para obtener datos de una página específica.
    
    Args:
        url (str): URL de la página a scrapear.
        nombres (list): Lista para almacenar los nombres de los productos.
        precios (list): Lista para almacenar los precios de los productos.
        marcas (list): Lista para almacenar las marcas de los productos.
        urls (list): Lista para almacenar los enlaces de los productos.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = soup.find_all('div', class_='ui-search-result__content-wrapper')

    for producto in productos:
        nombre = producto.find('h2', class_='ui-search-item__title').text
        precio = producto.find('span', class_='andes-money-amount__fraction').text
        link = producto.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link').get('href')

        # Inicializar la variable de resultado
        marca_encontrada = "OTROS"

        # Verificar si el nombre del producto contiene alguna de las marcas populares
        for marca in marcas_populares:
            if marca in nombre.upper():
                marca_encontrada = marca
                break
        
        # Agregar los datos a las listas
        nombres.append(nombre)
        precios.append(int(precio.replace('.', '')))
        marcas.append(marca_encontrada)
        urls.append(link)

def data_scrapping(url):
    """
    Función principal para realizar el scraping de datos desde un sitio web.
    
    Args:
        url (str): URL inicial del sitio web.
    
    Returns:
        DataFrame: Un DataFrame con los datos obtenidos.
    """
    nombres = []
    precios = []
    marcas = []
    urls = []

    # Variable para seguir la paginación
    url_actual = url

    while url_actual:
        logging.info(f"Scrapeando la página: {url_actual}")
        modelar_datos_pagina(url_actual, nombres, precios, marcas, urls)

        # Obtener la URL de la siguiente página
        response = requests.get(url_actual)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        siguiente_pagina = soup.find('a', class_='andes-pagination__link', title='Siguiente')
        
        if siguiente_pagina:
            url_actual = siguiente_pagina['href']
        else:
            url_actual = None  # No hay más páginas

    # Crear un DataFrame con los datos
    df = pd.DataFrame({
        'Nombre': nombres,
        'Precio': precios,
        'Marca': marcas,
        'Link': urls
    })
    output_path = 'data/precios_productos.csv'
    df.to_csv(output_path, index=False)
    logging.info(f"Datos guardados en {output_path}")
    return df

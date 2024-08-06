import scraping
import graphics
import logging

logging.basicConfig(level=logging.INFO)

def main():
    """
    Función principal para coordinar el scraping de datos y la generación de gráficos.
    """
    # URL inicial del sitio web (reemplazar con la URL real)
    url = 'https://listado.mercadolibre.com.ar/computacion/laptops-accesorios/notebooks/notebook_Desde_51_NoIndex_True'

    # Realizar el scraping de datos
    try:
        df = scraping.data_scrapping(url)
    except Exception as e:
        logging.error(f"Error al realizar el scraping de datos: {e}")
        return

    # Verificar si el DataFrame es válido
    if df is not None and not df.empty:
        # Normalizar los datos
        df_normalizado = graphics.normalize_data(df)

        # Generar los gráficos
        try:
            graphics.grafico_dispersion_precios(df_normalizado)
            graphics.grafico_histogramas_por_marca(df_normalizado)
            graphics.grafico_boxplot(df_normalizado)
            graphics.grafico_barras_marca(df_normalizado)
        except Exception as e:
            logging.error(f"Error al generar los gráficos: {e}")
    else:
        logging.error("El DataFrame obtenido está vacío o es None.")

if __name__ == "__main__":
    main()

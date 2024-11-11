import pandas as pd
import re
from model.pipeline.collection import load_data_from_db
from loguru import logger
from config.features_settings import FeaturesSettings

# Instancia de configuraciones para características
features_settings = FeaturesSettings()


def prepare_data() -> pd.DataFrame:
    """
    Realiza la preparación de datos, incluyendo carga, codificación y exclusión de columnas.

    Returns:
        pd.DataFrame: DataFrame con datos preprocesados.
    """
    logger.info('Iniciando la preparación de datos')

    try:
        # Cargar datos desde la base de datos
        logger.info('Cargando datos desde la base de datos...')
        data = load_data_from_db()
        logger.info('Datos cargados exitosamente desde la base de datos')
    except Exception as e:
        # Registro de error grave si falla la carga de datos
        logger.error(f'Error al cargar los datos desde la base de datos: {e}')
        raise  # Lanza de nuevo la excepción después de registrarla

    # Codificar columnas categóricas y extraer valores de columnas específicas
    data = encode_cat_cols(data)
    data = parse_col(data)

    # Excluir columnas según configuración
    exclude_columns = features_settings.exclude_columns
    logger.info(f'Excluyendo las columnas: {exclude_columns}')
    data = data[[col for col in data.columns if col not in exclude_columns]]
    logger.info('Pipeline de preprocesamiento completada')
    return data


def encode_cat_cols(data: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica las columnas categóricas, cambiando 'yes' a 1 y 'no' a 0.

    Args:
        data (pd.DataFrame): DataFrame con los datos a codificar.

    Returns:
        pd.DataFrame: DataFrame con columnas categóricas codificadas.
    """
    categorical_columns = features_settings.categorical_columns
    logger.info(f'Codificando variables categóricas: {categorical_columns}')
    data[categorical_columns] = data[categorical_columns].map(
        lambda x: 1 if x == 'yes' else 0
    )
    return data


def parse_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae el valor de metros cuadrados de las columnas especificadas.

    Args:
        data (pd.DataFrame): DataFrame con datos a parsear.

    Returns:
        pd.DataFrame: DataFrame con valores de área extraídos.
    """
    parse_columns = features_settings.parse_columns
    logger.info(f'Parseando las columnas: {parse_columns}')

    # Extraer el valor de área en metros cuadrados
    data[parse_columns] = data[parse_columns].apply(
        lambda x: int(re.search(r'(\d+)\s*m²', str(x)).group(1))  # type: ignore
        if re.search(r'(\d+)\s*m²', str(x)) else 0
    )
    return data

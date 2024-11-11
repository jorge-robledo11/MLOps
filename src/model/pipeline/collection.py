import pandas as pd
from sqlalchemy import select, create_engine
from sqlalchemy.exc import SQLAlchemyError
from databases.db_model import RentApartments
from config.db_settings import DBSettings
from loguru import logger

# Instanciar configuraciones de la base de datos y motor de conexión
db_settings = DBSettings()  # type: ignore
engine = create_engine(f'sqlite:///{db_settings.db_path}')


def load_data_from_db() -> pd.DataFrame:
    """
    Extrae datos de la tabla `RentApartments` desde la base de datos
    y los carga en un DataFrame.

    Returns:
        pd.DataFrame: DataFrame con los datos extraídos de la base de datos.

    Raises:
        SQLAlchemyError: Si ocurre un error al conectar o consultar la base de datos.
    """
    logger.info('Extrayendo la tabla de la base de datos')
    orm_query = select(RentApartments)

    try:
        # Ejecuta la consulta y carga los datos en un DataFrame
        with engine.connect() as connection:
            data = pd.read_sql(orm_query, connection)
        logger.info('Datos cargados exitosamente desde la base de datos')
        return data

    except SQLAlchemyError as e:
        # Manejo de errores en la conexión o consulta a la base de datos
        logger.error(f'Error al cargar datos desde la base de datos: {e}')
        raise

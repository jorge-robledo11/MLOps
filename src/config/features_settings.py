import yaml
from pydantic_settings import BaseSettings
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv, find_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv(find_dotenv(), override=True)


class FeaturesSettings(BaseSettings):
    """
    Configuración de características y propiedades del modelo de datos.

    Atributos:
        features_dir (str): Directorio que contiene los archivos de configuración de
            características.
        features_name (str): Nombre del archivo de configuración de características.
        categorical_columns (list[str]): Columnas categóricas para la codificación.
        exclude_columns (list[str]): Columnas que deben ser excluidas del modelo.
        parse_columns (list[str]): Columnas que necesitan un procesamiento adicional.
        features_prediction (list[str]): Columnas que se usan para predicciones.
        root_dir (Path): Directorio raíz del proyecto.
    """

    # Atributos específicos de los features
    features_dir: str
    features_name: str

    # Atributos para listas de columnas desde el archivo YAML
    categorical_columns: list[str] = list()
    exclude_columns: list[str] = list()
    parse_columns: list[str] = list()
    features_prediction: list[str] = list()

    # Atributo de directorio raíz usando pathlib
    root_dir: Path = Path(__file__).resolve().parents[1]

    def __init__(self, **kwargs):
        """
        Inicializa la clase FeaturesSettings y carga configuraciones adicionales desde
        un archivo YAML.

        Argumentos:
            **kwargs: Argumentos adicionales para la configuración de la clase.
        """
        super().__init__(**kwargs)

        # Cargar configuraciones adicionales desde un archivo YAML automáticamente
        try:
            logger.info(f'Cargando configuraciones de features desde {self.features_path}')
            with open(self.features_path, 'r') as file:
                data = yaml.safe_load(file)
                self.categorical_columns = data.get('categorical_columns', list())
                self.exclude_columns = data.get('exclude_columns', list())
                self.parse_columns = data.get('parse_columns', list())
                self.features_prediction = data.get('features_prediction', list())

        except FileNotFoundError:
            logger.error(f'El archivo de configuración {self.features_path} no se encontró.')

    @property
    def features_path(self) -> Path:
        """
        Devuelve la ruta completa del archivo de configuración de características.

        Returns:
            Path: Ruta completa del archivo de configuración de características.
        """
        return self.root_dir / self.features_dir / self.features_name

import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from config.model_settings import ModelSettings
from config.features_settings import FeaturesSettings
from loguru import logger

# Instancia de configuraciones para el modelo y las características
model_settings = ModelSettings()  # type: ignore
features_settings = FeaturesSettings()


class ModelInferenceService:
    """
    Clase que gestiona la carga y predicción de un modelo de Random Forest
    para predicciones basadas en características específicas.

    Métodos:
        load_model: Carga el modelo desde un archivo, construyéndolo si no existe.
        predict: Realiza predicciones usando el modelo cargado, dado un conjunto
        de características.
    """

    def __init__(self) -> None:
        """Inicializa el servicio del modelo, sin cargar el modelo en esta etapa."""
        self.model: RandomForestRegressor  # Inicializa el modelo sin asignarlo
        self.model_dir = model_settings.model_dir
        self.model_name = model_settings.model_name

    def load_model(self):
        """
        Carga el modelo desde el archivo especificado en las configuraciones.
        Si el archivo del modelo no existe, intenta construirlo y luego cargarlo.
        """
        model_path = model_settings.model_path
        logger.info(
            f'Comprobando la existencia del archivo del modelo en la ruta: {model_path}'
        )

        if not model_path.exists():
            raise FileNotFoundError('El modelo no existe')

        if model_path.exists():
            with model_path.open('rb') as file:
                self.model = pickle.load(file)
                logger.info('Modelo cargado exitosamente.')
        else:
            logger.error('No se pudo encontrar ni construir el modelo.')

    def predict(self, features: list) -> np.ndarray:
        """
        Realiza una predicción con el modelo cargado, dado un conjunto de características.

        Args:
            features (list): Lista de características para hacer la predicción.

        Returns:
            np.ndarray: Array de numpy con los resultados de la predicción.
                        Devuelve un array vacío si el modelo no está cargado.
        """
        features_df = pd.DataFrame(
            data=[features],
            columns=features_settings.features_prediction
        )
        logger.info('Haciendo predicción del modelo')

        if self.model:
            prediction = self.model.predict(features_df)
            return np.array(prediction)
        else:
            logger.error('El modelo no está cargado. No se puede hacer la predicción.')
            return np.array([])  # Array vacío en caso de error

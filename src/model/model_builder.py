from model.pipeline.model import build_model
from config.model_settings import ModelSettings
from loguru import logger

# Instancia de configuraciones para el modelo y las características
model_settings = ModelSettings()  # type: ignore


class ModelBuilderService:
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
        self.model_dir = model_settings.model_dir
        self.model_name = model_settings.model_name

    def train_model(self):
        """
        Entrenar el modelo desde la ruta especificada y guardarlo.
        """
        model_path = model_settings.model_path
        logger.info(
            f'Comprobando la existencia del archivo del modelo en la ruta: {model_path}'
        )
        build_model()

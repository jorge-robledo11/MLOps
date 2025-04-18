from model.model_inference import ModelInferenceService
from loguru import logger


@logger.catch
def main():
    logger.info('Ejecutando la aplicación')
    ml_svc = ModelInferenceService()
    ml_svc.load_model()
    unseen_data = [167.0, 1870.0, 3.0, 2.0, 2.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    pred = ml_svc.predict(unseen_data)
    logger.info(f'Predicción: {pred[0]:0.2f}')


if __name__ == '__main__':
    main()

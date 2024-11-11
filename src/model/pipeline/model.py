import pandas as pd
import pickle
from pathlib import Path
from model.pipeline.preparation import prepare_data
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from loguru import logger
from config.model_settings import ModelSettings

# Instancia de configuraciones para el modelo
model_settings = ModelSettings()  # type: ignore


def build_model():
    """
    Construye y entrena un modelo de Random Forest para la predicción de rentas,
    utilizando validación cruzada para la búsqueda de hiperparámetros.
    """
    logger.info('Empezamos la construcción de la pipeline')

    # Preparación de datos y separación en características y objetivo
    data = prepare_data()
    X, y = split_features_target(data)

    # División de los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    logger.info('División en conjuntos de entrenamiento y prueba completada')

    # Entrenamiento del modelo con hiperparámetros óptimos
    model = train_model(X_train, y_train)

    # Evaluación del modelo
    score = evaluate_model(model, X_test, y_test)
    logger.info(f'Evaluación del modelo completada, score: {score:0.2f}')

    # Guardado del modelo entrenado
    save_model(model)


def split_features_target(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Separa los datos en características (X) y variable objetivo (y).

    Args:
        data (pd.DataFrame): DataFrame con datos preprocesados.

    Returns:
        tuple: Una tupla (X, y) donde X son las características y y la variable objetivo.
    """
    X = data.loc[:, data.columns != 'rent']
    y = data.loc[:, data.columns == 'rent'].squeeze()
    logger.info('Separación de características y objetivo completada')
    return X, y


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series
) -> RandomForestRegressor:
    """
    Entrena un modelo de Random Forest utilizando GridSearchCV para optimizar
    los hiperparámetros con validación cruzada.

    Args:
        X_train (pd.DataFrame): Conjunto de características de entrenamiento.
        y_train (pd.Series): Variable objetivo de entrenamiento.

    Returns:
        RandomForestRegressor: El mejor modelo entrenado según la búsqueda.
    """
    grid_space = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 6, 9, 12]
    }
    logger.debug(f'Parámetros de búsqueda: {grid_space}')

    model = GridSearchCV(
        RandomForestRegressor(random_state=123),
        param_grid=grid_space,
        cv=5,
        scoring='r2'
    )
    model.fit(X_train, y_train)
    logger.info('Entrenamiento del modelo completado')
    return model.best_estimator_


def evaluate_model(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> float:
    """
    Evalúa el modelo en el conjunto de prueba y retorna el puntaje R².

    Args:
        model (RandomForestRegressor): Modelo entrenado.
        X_test (pd.DataFrame): Características de prueba.
        y_test (pd.Series): Variable objetivo de prueba.

    Returns:
        float: Puntaje R² del modelo.
    """
    score = model.score(X_test, y_test)
    return score  # type: ignore


def save_model(model: RandomForestRegressor) -> None:
    """
    Guarda el modelo entrenado en la ubicación especificada en las configuraciones.

    Args:
        model (RandomForestRegressor): Modelo entrenado a guardar.
    """
    model_dir = Path(model_settings.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_settings.model_path
    with model_path.open('wb') as file:
        pickle.dump(model, file)

    logger.info(f'Modelo guardado en el directorio: {model_path}')

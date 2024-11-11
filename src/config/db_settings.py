from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Cargar el archivo .env explícitamente usando find_dotenv
load_dotenv(find_dotenv())


class DBSettings(BaseSettings):
    """
    Configuración de la base de datos.

    Atributos:
        db_dir (str): Directorio que contiene el archivo de la base de datos.
        db_name (str): Nombre del archivo de la base de datos.
        table_name (str): Nombre de la tabla en la base de datos.
        root_dir (Path): Ruta al directorio raíz del proyecto.
    """

    # Atributos de directorios y archivos
    db_dir: str  # Directorio de la base de datos
    db_name: str  # Nombre de la base de datos
    table_name: str  # Nombre de la tabla en la base de datos

    # Atributo de directorio raíz usando pathlib
    root_dir: Path = Path(__file__).resolve().parents[1]

    @property
    def db_path(self) -> Path:
        """
        Devuelve la ruta completa al archivo de la base de datos.

        Returns:
            Path: Ruta completa al archivo de la base de datos.
        """
        return self.root_dir / self.db_dir / self.db_name

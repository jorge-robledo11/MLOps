# Declarar que estos objetivos no representan archivos sino tareas a ejecutar siempre
.PHONY: run_builder run_builder inference install clean check builder inference

# Definir el objetivo predeterminado cuando se ejecuta `make` sin especificar un objetivo
.DEFAULT_GOAL := inference

# Objetivo para ejecutar la aplicación
# Primero ejecuta el objetivo `install` para asegurar que las dependencias estén instaladas
run_builder: install
	cd src && poetry run python builder.py

run_inference: install
	cd src && poetry run python inference.py

# Objetivo para instalar dependencias usando Poetry
# Se asegura de que `pyproject.toml` esté presente antes de instalar
install: pyproject.toml
	poetry install --without dev

# Objetivo para limpiar archivos temporales, como carpetas de caché de Python
clean:
	rm -rf `find . -type d -name __pycache__`

# Objetivo para verificar la calidad del código con Flake8
check:
	poetry run flake8 src/

# Objetivo `runner` que ejecuta una secuencia de objetivos: check, run y clean
# Primero verifica la calidad del código, luego ejecuta la aplicación, y finalmente limpia archivos temporales
builder: check run_builder clean
inference: check run_inference clean

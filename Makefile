# Declarar que estos objetivos no representan archivos sino tareas a ejecutar siempre
.PHONY: run install clean check runner

# Definir el objetivo predeterminado cuando se ejecuta `make` sin especificar un objetivo
.DEFAULT_GOAL := runner

# Objetivo para ejecutar la aplicación
# Primero ejecuta el objetivo `install` para asegurar que las dependencias estén instaladas
run: install
	cd src && poetry run python main.py

# Objetivo para instalar dependencias usando Poetry
# Se asegura de que `pyproject.toml` esté presente antes de instalar
install: pyproject.toml
	poetry install --only main

# Objetivo para limpiar archivos temporales, como carpetas de caché de Python
clean:
	rm -rf `find . -type d -name __pycache__`

# Objetivo para verificar la calidad del código con Flake8
check:
	poetry run flake8 src/

# Objetivo `runner` que ejecuta una secuencia de objetivos: check, run y clean
# Primero verifica la calidad del código, luego ejecuta la aplicación, y finalmente limpia archivos temporales
runner: check run clean

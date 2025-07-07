#Directory
TEST_DIR = test

#Format + Linting
lint:
	@echo Format + Linting
	@ruff check . --fix

#DeepCheck
deepcheck:
	@echo Launch DeepCheck
	@mypy --config mypy.ini

# Run the pipeline training
model:
	@echo Launch training
	@py model.py

# Start MLflow Server
mlflow_server:
	@echo Start MLflow server
	@mlflow ui

# See Models in BentoML
bentoml:
	@echo Start BentoML server
	@py -m  bentoml models list
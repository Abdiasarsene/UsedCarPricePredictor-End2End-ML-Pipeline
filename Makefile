#Directory
TEST_DIR = test

#Format + Linting
lint:
	@echo "Format + Linting"
	@ruff check . --fix

#Format
format:
	@echo Format du code 
	@ruff check .

# Run the pipeline training
model:
	@echo "Launch training"
	@py model.py

# Start MLflow Server
mlflow_servver:
	@echo "Start MLflow server
	@mlflow ui

# See Models in BentoML
bentoml_models:
	@echo "Start BentoML server
	@py -m  bentoml models list


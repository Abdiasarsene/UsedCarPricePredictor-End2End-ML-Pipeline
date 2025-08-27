.PHONY: lint mypy model mlflow bentoml cat_cols cyclo code

# Directories
TEST_DIR = test
TRAINER_DIR = trainer
API_DIR = app

# Default
default: lint cyclo code mypy
	@echo "Default pipeline done"

# Format + Linting
lint:
	@echo "Format + Linting"
	@ruff check . --fix

# Static Type Checking
mypy:
	@echo "Running mypy type checks"
	@mypy --config mypy.ini

# Run the pipeline training
model:
	@echo "Launch training"
	@python runner.py

# Start MLflow Server
mlflow:
	@echo "Start MLflow server"
	@mlflow ui

# See Models in BentoML
bentoml:
	@echo "List models in BentoML"
	@python -m bentoml models list

# Extract single modalities in each cat col
cat_cols:
	@echo "Starting extraction"
	@python $(TRAINER_DIR)/extract_cols.py

# Cyclomatic Complexity Analysis
cyclo:
	@echo "Cyclo Analysis"
	@radon mi $(API_DIR)/ $(TRAINER_DIR)/ -s

# Security Code Analysis
code:
	@echo "Code Analysis"
	@bandit -r $(API_DIR)/ $(TRAINER_DIR) -ll

# Launch API
api:
	@echo "Launch API"
	@uvicorn main:app --reload
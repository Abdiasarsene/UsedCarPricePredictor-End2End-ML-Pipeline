#Importation  des  libraires nécessaires
import os
from dotenv import load_dotenv

load_dotenv()
# ====== Fonction d'appel des fichiers ======
class Settings():
	def __init__(self):
		self.dataset = os.getenv("DATASET_PATH")
		self.mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
		self.mlflow_experiment = os.getenv("MLFLOW_EXPERIMENT")

settings = Settings()


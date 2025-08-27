# runner.py
import time
import mlflow
import logging
import traceback
from trainer.config import settings
from trainer.loaders.data_loader import load_and_encode
from trainer.preprocessing.preprocessing import get_preprocessing
from trainer.models.training import train_models
from trainer.evauation.predEvalSave import predict_evaluate_save
from trainer.monitor.monitor import (
    log_data_info,
    log_preprocess_info,
    log_train_info,
    log_backup_info
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialisation MLflow
        mlflow.set_tracking_uri(settings.mlflow_uri)
        mlflow.set_experiment(settings.mlflow_experiment)
        logger.info("✅ Initialization done")
        
        with mlflow.start_run(run_name="UsedCarPrice"):

            # Chargement et encodage des données
            x_train, x_test, y_train, y_test, usedcar = load_and_encode()
            log_data_info(usedcar)

            # Préprocessing
            preprocessor = get_preprocessing(usedcar)

            # Correction : .columns est un attribut, pas une méthode
            num_cols = usedcar.select_dtypes(include=["float64", "int64"]).columns.tolist()
            cat_cols = usedcar.select_dtypes(include=["object"]).columns.tolist()
            log_preprocess_info(num_cols, cat_cols)

            # Entraînement
            start_time = time.time()
            trained_models = train_models(x_train, y_train, preprocessor)
            duration = time.time() - start_time

            # Correction : il faut itérer sur trained_models, pas sur la fonction
            for model_name in trained_models:
                log_train_info(model_name, duration)

            # Prédiction, évaluation et sauvegarde
            evaluation_results = predict_evaluate_save(trained_models, x_test, y_test)
            log_backup_info(evaluation_results)

    except Exception as e:
        logger.error(f"❌ Error Detected: {str(e)}")
        logger.debug(f"⚠️ Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()

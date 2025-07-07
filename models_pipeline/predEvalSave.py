# Importing required libraries
import logging
import mlflow
import bentoml
import numpy as np
from models_pipeline.config import settings
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== EVALUATION FUNCTION ======
def evaluate_model(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return rmse, mae, mape

# ====== PREDICT + EVAL + SAVE FUNCTION FOR TOP 3 MODELS ======
def predict_evaluate_save(x_test, y_test, trained_models):
    try:
        for model_name, model in trained_models.items():
            logger.info("🚀 Starting prediction process")

            # Predict with the best model already inside the pipeline
            y_pred = model.predict(x_test)
            rmse, mae, mape = evaluate_model(y_test, y_pred)
            logger.info(f"✅ Predictions done with {model_name}")
            
            # MLflow setup
            mlflow.set_tracking_uri(settings.mlflow_uri)
            mlflow.set_experiment(settings.mlflow_experiment)

            with mlflow.start_run(run_name=model_name):
                logger.info("🏷️ Logging metrics for each model")
                mlflow.log_metrics({
                    "RMSE": rmse,
                    "MAE": mae,
                    "MAPE": mape
                })
                
                logger.info("🏷️ Save each model via MLflow")
                mlflow.sklearn.log_model(model, model_name)
                logger.info("✅ Model logged to MLflow")
                
                
                # Save the model into Model Registry
                model_uri = mlflow.register_model(
                    model_uri=f"runs:/{mlflow.active_run().info.run_id}/{model_name}",
                    name=model_name
                )
                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=model_name,
                    version=model_uri.version,
                    stage="Production",
                    archive_existing_versions=True
                )
                logger.info(f"✅ Model registered in MLflow Model Registry with URI: {model_uri}")

            # Save with BentoML
            bentoml.sklearn.save_model(
                model_name, 
                model,
                signatures={"predict": {"batchable": True}},
            )
            logger.info("🧊 Model saved with BentoML")
    except Exception as e:
        logger.error(f"❌❌ Error during prediction/evaluation/saving: {e}")
        raise e
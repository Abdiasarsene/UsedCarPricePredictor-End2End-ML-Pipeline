# Importng libriairies required
import logging
import mlflow
import bentoml
import numpy as np
from models_pipeline.config import settings
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# ====== LOGGING ======
logging.basicConfig(logging.INFO)
logger = logging.getLogger(__name__)

# ====== EVALUATION FUNCTION ======
def evaluate_model(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return rmse, mae, mape

# ====== PREDICT + EVAL + SAVE ======
def predict_evaluate_save(x_test, y_test, pipeline):
    try :
        logger.info("🚀 Starting prediction")
        y_pred = pipeline.predict(x_test)
        
        logger.info("📊 Calculating metrics...")
        rmse, mae, mape = evaluate_model(y_test, y_pred)
        logger.info(f"📉 RMSE : {rmse:.2f}")
        logger.info(f"📈 MAE : {mae:.2f}")
        logger.inof(f"📉 MAPE: {mape:.2f}")
        
        # Mlflow Setup
        mlflow.set_tracking_uri(settings.mlflow_uri)
        mlflow.set_experiment(settings.mlflow_experiment)
        
        with mlflow.start_run():
            mlflow.log_metrics("RMSE",rmse)
            mlflow.log_metric("MAE",mae)
            mlflow.log_metric("MAPE",mape)
            
            # Save the pipeline as artifact
            mlflow.sklearn.log_model(pipeline, "model")
            logger.info("✅✅ Model logged to MLflow")
        
        # Save with BentoML
        bentoml.sklearn.save_model(
            name ="usedcar_model",
            model=pipeline,
            signatures={"predict":{"batchable":True}},
            metadata={"RMSE": rmse, "MAE": mae, "MAPE": mape}
        )
        logger.info("🧊 Model saved with BentoML")
    
    except Exception as e:
        logger.error(f"❌❌ Error during prediction/evaluation/saving: {e}")
        raise e
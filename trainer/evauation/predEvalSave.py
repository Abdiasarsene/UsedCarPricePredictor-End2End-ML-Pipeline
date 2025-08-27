# Importing required libraries
import logging
import traceback
import numpy as np
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
        # Dico to save metrics and model 
        result = {}
        
        # Loop
        for name, model in trained_models.items():
            # Prediction
            y_pred = model.predict(x_test)
            logger.info("✅ Prediction done")
            
            # Evaluation
            rmse, mae, mape = evaluate_model(y_pred, y_test)
            logger.info("✅ Evaluation also done")
            
            # Save
            result[name] = {
                "model": model, 
                "metrics":{
                    "RMSE":rmse, 
                    "MAE": mae, 
                    "MAPE": mape
                }
            }
            logger.info("✅ Predict + Evaluate + Save")
            return result
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"⚠️ Traceback complete : {traceback.format_exc()}")
        raise e

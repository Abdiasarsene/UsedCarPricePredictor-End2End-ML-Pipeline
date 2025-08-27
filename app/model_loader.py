# Modules required
import logging
import traceback
import mlflow
import bentoml
from app.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== FUNCTION OF MLFLOW ======
def load_mlflow_model(path):
    try:
        # Initialize
        mlflow.set_tracking_uri(settings.tracking_uri)
        logger.info(f"Tracking Used : {settings.tracking_uri}")
        
        # Mlflow loaded
        model = mlflow.pyfunc.load_model(path)
        if model is None:
            raise RuntimeError("⚠️ Mlflow failed")
        logger.info("✅ Mlflow loaded")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"⚠️ Traceback : {traceback.format_exc()}")

# ====== FUNCTION OF BENTOML ======
def load_bentoml_model(tag):
    try:
        model = bentoml.sklearn.load_model(tag)
        if model is None:
            raise RuntimeError("⚠️ BentoML failed")
        logger.info("🔃 BentoML loaded")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"⚠️ Traceback : {traceback.format_exc()}")
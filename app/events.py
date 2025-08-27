# api/events.py
import logging
import traceback
import asyncio
from fastapi import FastAPI

from .model_loader import load_mlflow_model, load_bentoml_model
from .config import settings

# ====== LOGGING ======
logger = logging.getLogger(__name__)

# ====== SETTINGS ======
model = None
model_type = None

# ======= LOADED MODELS ======
def get_model():
    return model, model_type

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_events():
        global model, model_type
        logger.info("🚀 API Starting — loading model...")

        try:
            # MLflow loading
            logger.info("🔃 Trying MLflow model...")
            model = await asyncio.wait_for(
                asyncio.to_thread(load_mlflow_model, settings.xgboost_mlflow),
                timeout=10.0
            )
            model_type = "MLflow"
            logger.info("✅ MLflow model loaded")

        except Exception as mlflow_error:
            logger.error(f"❌ MLflow load failed: {mlflow_error}")
            logger.debug(f"Traceback : {traceback.format_exc()}")

            # BentoML Fallback
            try:
                logger.info("🔃 Falling back to BentoML...")
                model = load_bentoml_model(settings.bentoml_model)
                model_type = "BentoML"
                logger.info(f"✅ BentoML model loaded: {type(model).__name__}")
            except Exception as bentoml_error:
                logger.critical(f"❌ Fallback BentoML also failed: {bentoml_error}")
                logger.debug(f"Traceback : {traceback.format_exc()}")

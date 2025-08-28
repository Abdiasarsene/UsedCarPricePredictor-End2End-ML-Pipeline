# api/events.py
import logging
import asyncio
from fastapi import FastAPI

from .model_loader import load_mlflow_model, load_bentoml_model
from .config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======= LOADED MODELS ======
def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_events():
        logger.info("🚀 API Starting — loading model...")
        
        try:
            logger.info("🔃 Trying MLflow model...")
            model = await asyncio.to_thread(load_mlflow_model, settings.lineareg_mlflow)
            app.state.model = model
            app.state.model_type = "MLflow"
            logger.info("✅ MLflow model loaded")
            
        except Exception as mlflow_error:
            logger.error(f"❌ MLflow load failed: {mlflow_error}")
            logger.exception("Stack trace : ")
            
            try:
                logger.info("🔃 Falling back to BentoML...")
                model = load_bentoml_model(settings.bentoml_model)
                app.state.model = model
                app.state.model_type = "BentoML"
                logger.info(f"✅ BentoML model loaded: {type(model).__name__}")
            
            except Exception as bentoml_error:
                logger.critical(f"❌ Fallback BentoML also failed: {bentoml_error}")
                logger.exception("Stack trace : ")
                app.state.model = None
                app.state.model_type = None
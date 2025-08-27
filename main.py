# Modules required imported
from fastapi import FastAPI
import logging

from app.config import settings
from app.events import register_startup_event
from app.routes.routes import router as app_router
from app.monitor import add_monitoring, metrics_middleware
from app.secure import apply_security_middleware

# ====== SETUP LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
        app = FastAPI(
            title=str(settings.api_title),
            version=str(settings.api_version),
            description=str(settings.api_description)
        )
        
        # Middleware Security
        apply_security_middleware(app)
        
        # Monitoring (Prometheus)
        add_monitoring(app)
        app.middleware(str(settings.protocol))(metrics_middleware)
        
        # Startup event : Model loaded
        register_startup_event(app)
        
        # Router app
        app.include_router(app_router)
        
        logger.info("✅ FastAPI APP Created and Configured")
        return app

app = create_app()
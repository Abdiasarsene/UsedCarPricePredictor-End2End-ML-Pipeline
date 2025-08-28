# Modules required imported
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .config import settings
import logging

oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.token)

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MIDDLLEWARE SETUP ======
def apply_security_middleware(app:FastAPI):
    try:
        app.add_middleware(
            CORSMiddleware, 
            allow_origins=[''],
            allow_credentials=True, 
            allow_methods=['*'],
            allow_headers=['*']
        )
        
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[settings.local_test,settings.domain_name]
        )
        logger.info("✅ Middleware Applied")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")

# ====== TOKEN CHECKER ======
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        if token != settings.token_two:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or missing token",
                headers={"WWW-Authenticate" : "Bearer"}
            )
            logger.info("✅ Token succeded")
            return {"user" : "authenticated"}
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace :")
# Modules required imported
from fastapi import APIRouter, HTTPException, Request
from app.schemas.schema import CarPriceData
from app.services.predictor import make_prediction
from app.monitor import increment_inference_count
import logging

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", redirect_slashes=False)

# ====== ROUTE OF PREDICTON =====
@router.post("/predict")
async def predict_car(data: CarPriceData, request: Request):
    try:
        logger.info("🔃 Starting of prediction")
        model = getattr(request.app.state, "model", None)
        model_type = getattr(request.app.state, "model_type", None)
        if model is None:
            raise HTTPException(status_code=500, detail="❌ Model not loaded")
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)
        
        increment_inference_count()
        logger.info("🚀 Prediction done")
        
        return {
            "Deliver Status": message,
            "Code": predicted_class,
            "Statut": "Success",
            "Model Used": model_type
        }
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")
        raise HTTPException(status_code=500, detail=str(e))


# ====== ROUTE OF VALIDATION ======
@router.post("/validate")
async def validate_car_input(data: CarPriceData):
    try:
        logger.info("🔎 Validation of input data")
        validated_data = data.model_dump(by_alias=True)
        logger.info("🟢 Data Checked")
        return {
            "Validated Data" : validated_data,
            "Message" : "Input Data Matcher",
            "Statut" : "Success"
        }
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace")
        raise HTTPException(status_code=400, detail=f"❌ Validation Error ; {str(e)}")

# ====== DEBUG ======
@router.post("/debug")
async def debug_request(request: Request):
    headers = dict(request.headers)
    try:
        body = await request.json()
    except Exception as e:
        body = f"Invalid JSON: {e}"
    return {"headers": headers, "body": body}

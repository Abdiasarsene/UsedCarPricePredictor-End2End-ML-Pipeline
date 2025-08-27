# Modules required imported
from fastapi import APIRouter, HTTPException
from ..schemas.schema import CarPriceData
from ..services.predictor import make_prediction
from ..events import get_model
from ..monitor import increment_inference_count
import logging
import traceback

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", redirect_slashes=False)

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
        logger.debug(f"🟢 Traceback : {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"❌ Validation Error ; {str(e)}")

# ====== ROUTE OF PREDICTON =====
@router.post("/predict")
async def predict_car(data: CarPriceData):
    try:
        # Prediction + Print of message
        logger.info("🔃 Starting of prediction")
        model, model_type = get_model()
        if model is None:
            raise HTTPException(status_code=500, detail="❌ Model not loaded")
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)
        increment_inference_count()
        logger.info("🚀 Prediction done")
        
        # Printing of message
        return {
            "Deliver Status" : message, 
            "Code" : predicted_class,
            "Statut" : "Success",
            "Model Used" : model_type
        }
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"🟢 Traceback :{traceback.format_exc()}")

# Modules requied
import logging
import pandas as pd

# ====== LOGGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======== MESSAGE OUTPUT BEFORE PREDICTOR =======
def format_price_message(predicted_price:float, currency: str="€") -> str :
    base_question = "💰 Estimated resale price af the car"
    
    # Round off and convert nicely
    formatted_price = f"{predicted_price:,.2f}".replace(","," ")

    # Categorize (optional)
    if predicted_price < 30000:
        response = f"{formatted_price}{currency} 🚗 - Low price range. Might be an old or basic model"
    elif predicted_price < 150000:
        response = f"{formatted_price}{currency} 🚙 - Mid range price. Seems like a fair deal."
    else: 
        response = f"{formatted_price}{currency} 🚓 High-end value. Likely a premium or recent car."
    return f"{base_question} : {response}"

# ====== PREDICTION FUNCTION ======
def make_prediction(model, model_type: str, input_dict: dict) -> tuple[float, str]:
    try:
        df = pd.DataFrame([input_dict])
        
        if model_type in ['MLflow', 'BentoML']:
            prediction = model.predict(df)
            predicted_prices = float(prediction[0])
        else:
            predicted_prices = 0.0  # fallback if model_type unknown

        message = format_price_message(predicted_prices)
        return predicted_prices, message    

    except Exception as e:
        logger.error(f"❌ Error Detected: {str(e)}")
        logger.exception("Stack trace")
        # Return default tuple on error
        return 0.0, "❌ Prediction failed due to an error."

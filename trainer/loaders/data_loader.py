# Importing libriaires
import logging
import traceback
import pandas as pd
from trainer.config import settings
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logger = logging.getLogger()

# ====== LOADING + ENCODING + SPLIT ======
def load_and_encode():
    try:
        # Loading of dataset
        usedcar = pd.read_csv(settings.dataset)
        logger.info("✅ Data loaded successfully")
        
        # Preparing features
        x = usedcar.drop(columns=settings.target)
        y = usedcar[settings.target]
        
        # Split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        logger.info("✅ Successful split")
        return x_train, x_test, y_train, y_test, usedcar
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"⚠️Traceback complete : {traceback.format_exc()}")
        raise e

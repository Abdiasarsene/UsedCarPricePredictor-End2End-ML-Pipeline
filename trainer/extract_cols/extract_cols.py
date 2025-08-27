# Modules required Imports
import os 
import json
import logging
import traceback
import pandas as pd
from dotenv import load_dotenv

# Variable d'envi and Logging 
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function
try:
        # Import Data
        data = os.getenv("DATASET_PATH")
        xlsx_data = pd.read_csv(data)
        logger.info("✅ Data Loaded")
        
        # Extract only categoricals cols
        cat_cols = xlsx_data.select_dtypes(include=["object"]).columns.tolist()
        
        # Extract unique modals in each cat cols
        categories = {
            col : xlsx_data[col].dropna().unique().tolist()
            for col in cat_cols
        }
        
        # Download the file
        with open("../dataset/categories_modals.json", "w") as f: 
            json.dump(categories, f, indent=4)
        logger.info("✅ Extracted single modalities")

except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"🟢 Traceback : {traceback.format_exc()}")


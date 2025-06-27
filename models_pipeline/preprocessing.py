# Importing libraies required
import logging
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from category_encoders import CatBoostEncoder
from sklearn.impute import KNNImputer,SimpleImputer
from sklearn.compose import ColumnTransformer

# ====== LOGGING ======
logger = logging.getLogger()

# ====== GET PREPROCESSING ======
def get_preprocessing(usedcar):
    try:
        features = usedcar.drop(columns=['Price'])
        
        # Separating numericals and categoricals features
        num_cols = features.select_dtype(include=["int","float"]).columns.tolist()
        cat_cols = features.select_dtypes(include=["object"]).columns.tolist()
        
        # Preprocessing
        num_transformers = Pipeline([
            ('impute', KNNImputer(n_neighbors=3)),
            ("scaler", RobustScaler())
        ])
        
        cat_transformers = Pipeline([
            ('impute', SimpleImputer(strategy='most_frequent')),
            ('encode', CatBoostEncoder())
        ])
        
        preprocessor = ColumnTransformer([
            ('num', num_transformers,num_cols),
            ('cat', cat_transformers, cat_cols)
        ])
        logger.info('✅✅ Preprocessing successfully did')
        return preprocessor
    except Exception as e:
        logger.error(f"Troublles : {e}")
        raise e
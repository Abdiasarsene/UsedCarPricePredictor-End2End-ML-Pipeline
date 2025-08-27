# Importing libraries required
import logging
import traceback
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== TRAINING FUNCTION ======
def train_models(x_train, y_train, preprocessor):
    try:
        models = {
            'linearreg': LinearRegression(
                fit_intercept=True,
                # normalize='deprecated',  
                n_jobs=-1
            ),
            
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42,
                n_jobs=-1
            ),
            
            'svr': SVR(
                kernel='rbf',
                C=1.0,
                epsilon=0.1,
                gamma='scale'
            ),
            
            'decision_tree': DecisionTreeRegressor(
                criterion='squared_error',
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42
            )
        }

        # Dictionary to store trained models
        trained_models = {}

        for name, model in models.items():
            try:
                pipeline = Pipeline([
                    ('preprocessor', preprocessor),
                    ('model', model)
                ])

                pipeline.fit(x_train, y_train)

                trained_models[name] = pipeline
                logger.info(f"Model {name} trained successfully.")
            except Exception as e:
                logger.error(f"❌ Error Detected :{name}: {e}")
                logger.debug(f"⚠️ Traceback complete : {traceback.format_exc()}")

        logger.info("All models trained successfully.🚀🚀")
        return trained_models
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"⚠️ Traceback complete : {traceback.format_exc()}")
        raise e

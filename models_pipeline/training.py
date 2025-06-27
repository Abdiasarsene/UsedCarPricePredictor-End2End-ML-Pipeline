# Importing libraries
import logging
from flaml import AutoML
from sklearn.pipeline import Pipeline

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== TRAINING FUNCTION ======
def train_models(x_train, y_train, preprocessor):
    try:
        automl = AutoML()
        automl_settings = {
            "time_budget": 300,
            "task": "regression",
            "metric": "mae",
            "estimator_list": ["xgboost", "rf", "lgbm"],
            "log_file_name": "automl.log",
            "verbosity": 1
        }

        pipeline = Pipeline([
            ("preprocessing", preprocessor),
            ("automl", automl)
        ])

        # ✅ Double underscore syntax
        pipeline.fit(x_train, y_train, **{f'automl__{k}': v for k, v in automl_settings.items()})
        logger.info("✅✅ Training successfully done")

        # Access trained AutoML instance
        automl = pipeline.named_steps['automl']

        # ✅ Correct spelling and loop
        for estimator_name, config in automl.best_config_per_estimator.items():
            logger.info(f"✅ Trained estimator: {estimator_name} with config: {config}")

        # ✅ Singular form
        logger.info(f"🏆 Best model selected: {automl.best_estimator}")
        logger.info(f"📉 Best validation MAE: {automl.best_loss}")

        return pipeline

    except Exception as e:
        logger.error(f"❌❌ Training failed: {e}")
        raise e

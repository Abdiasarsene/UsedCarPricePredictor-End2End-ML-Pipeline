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
            "log_file_name": "automl.log"
        }

        pipeline = Pipeline([
            ("preprocessing", preprocessor),
            ("automl", automl)
        ])

        # Fit with settings
        pipeline.fit(x_train, y_train, **{f'automl__{k}': v for k, v in automl_settings.items()})
        logger.info("✅✅ Training successfully done")

        # Access AutoML instance
        automl = pipeline.named_steps['automl']

        # ✅ Safe version (without learning_curve)
        top_3 = list(automl.best_config_per_estimator.items())[:3]

        logger.info("🎯 Top 3 models (from best_config_per_estimator):")
        for rank, (estimator_name, config) in enumerate(top_3, 1):
            logger.info(f"#{rank}: {estimator_name} | Config: {config}")

        # Log the overall best model separately
        logger.info(f"🏆 Best overall model: {automl.best_estimator}")
        logger.info(f"📉 Best validation MAE: {automl.best_loss}")

        return pipeline

    except Exception as e:
        logger.error(f"❌❌ Training failed: {e}")
        raise e

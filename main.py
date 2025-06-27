# Importing of librairies required
from models_pipeline.data_loader import load_and_encode
from  models_pipeline.preprocessing import get_preprocessing
from models_pipeline.training import train_models
from models_pipeline.predEvalSave import predict_evaluate_save

# Launch of the main function
if __name__ == "__main__":
	# Loading + encoding 
	x_train, x_test, y_train, y_test, usedcar = load_and_encode()

	# Starting the preprocessing
	preprocessor = get_preprocessing(usedcar)

	# Run the training
	pipeline = train_models(x_train, y_train, preprocessor)

	# Prediction + Evaluation + Backup
	predict_evaluate_save(x_test, y_test, pipeline)

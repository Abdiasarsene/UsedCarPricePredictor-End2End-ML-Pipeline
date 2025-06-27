# 🎯 UsedCarPricePredictor — ML-Powered Price Estimation API for Used Cars

UsedCarPricePredictor is a production-grade, modular MLOps pipeline designed to deliver **accurate, explainable resale price predictions** for used cars.
Built to streamline pricing decisions in the automotive marketplace, it provides a robust backend API leveraging AutoML, scalable preprocessing, and model versioning with MLflow and BentoML.

---

## 🧠 Project Purpose

Tailored for automotive businesses, data scientists, and marketplaces seeking to:

* Predict used car prices with strong accuracy and robustness
* Handle heterogeneous data: numerical, categorical with many modalities
* Automate training, evaluation, and deployment workflows
* Maintain reproducibility with data & model versioning
* Deliver an easy-to-use API for integration in apps or platforms

---

![UsedCarPricePredictor API](./statics/api_screenshot.png)

---

## 🧰 Tech Stack

| Area                   | Tools & Frameworks                                    |
| ---------------------- | ----------------------------------------------------- |
| Data Versioning        | DVC                                                   |
| Preprocessing          | Scikit-learn Pipelines, RobustScaler, CatBoostEncoder |
| Modeling               | FLAML (AutoML with XGBoost, LightGBM, Random Forest)  |
| Experiment Tracking    | MLflow (local & remote registry)                      |
| Model Packaging        | BentoML                                               |
| API Serving            | FastAPI (via BentoML runtime)                         |
| CI/CD                  | Makefile, GitHub Actions (optional)                   |
| Monitoring             | MLflow dashboards, (Prometheus + Grafana - planned)   |
| Testing                | Pytest                                                |
| Containerization       | Docker, docker-compose                                |
| Environment Management | Python virtualenv, python-dotenv                      |

---

## 🏗️ Project Structure

```
UsedCarPricePredictor/
│
├── models_pipeline/         # Core source code (data, preprocessing, training, inference)
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── training.py
│   ├── predEvalSave.py
│
├── data/                    # Raw and processed datasets (tracked by DVC)
│   └── used_cars.csv
│
├── models/                  # Saved ML models (MLflow & BentoML)
│
├── notebooks/               # EDA and experimentation
│
├── tests/                   # Unit and integration tests
│
├── main.py                  # Orchestrates training and prediction
├── requirements.txt
├── README.md
├── dvc.yaml                 # Optional DVC pipeline stages
└── Makefile                 # For common commands (train, test, run, deploy)
```

---

## 🔁 MLOps Workflow

1. **Data versioning** with `DVC` to ensure dataset reproducibility
2. **Advanced preprocessing**:

   * Outlier-robust scaling (`RobustScaler`)
   * Handling categorical features with high cardinality (`CatBoostEncoder`)
3. **AutoML-powered training** using `FLAML` to automatically select the best model & hyperparameters
4. **Experiment tracking** and model registration in `MLflow`
5. **Model packaging** using `BentoML` for easy API deployment
6. **Serving the model** via a FastAPI endpoint managed by BentoML
7. **Continuous monitoring & testing** to ensure model performance and data quality over time (planned)

---

## 🔄 Continuous Training (Roadmap)

* Automate retraining triggered by new data
* Model comparison and automatic promotion only if performance improves
* CI/CD integration to seamlessly deploy updated models

---

## 📊 Evaluation Metrics

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* Mean Absolute Percentage Error (MAPE)

---

## ✅ Makefile commands

```bash
make train       # Train and log with MLflow
make test        # Run tests
make serve       # Start BentoML API server
make deploy      # Build and push Docker containers
make format      # Code formatting and linting
```

---

## 🤝 Contribution

This repo is an evolving production-grade pipeline crafted by **Abdias Arsène**.
Contributions are welcome but please open an issue or PR with clear descriptions.

---

## 🔗 About

Built by Abdias Arsène,
IT Consultant in AI & MLOps — building data-driven solutions with impact across health, humanitarian, finance, and now automotive.

> *“I don’t just write code to run. I write code to endure.”*

---

![MLflow & BentoML](./statics/mlflow_bentoml.png)

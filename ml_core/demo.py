# ml_core/demo.py
from algorithms.classical import get_classical_model
from data_handlers.load_dataset import load_data
from sklearn.metrics import classification_report
from evaluation.metrics import EvaluationReport

if __name__ == "__main__":
    dataset = load_data("sinx")  

    print("Meta:", dataset.meta)
    
    params_for_xgboost = {
    "n_estimators": 500,
    "learning_rate": 0.03,
    "max_depth": 3,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    }

    params_svm = {"kernel": "linear"}

    model = get_classical_model("svm",dataset.meta.task)
    model.fit(dataset.X_train, dataset.y_train)
    pred = model.predict(dataset.X_test)

    print(pred)
    report = EvaluationReport(dataset.y_test, pred, dataset.meta.task, target_names=dataset.meta.class_labels)
    print(report.report_str())

# ml_core/demo.py
from algorithms.classical import get_classical_model
from data_handlers.load_dataset import load_data
from sklearn.metrics import classification_report
from evaluation.metrics import EvaluationReport

if __name__ == "__main__":
    dataset = load_data("diabetes")  

    print("Meta:", dataset.meta)
    
    params = {}

    model = get_classical_model("xgboost",dataset.meta.task)
    model.fit(dataset.X_train, dataset.y_train)
    pred = model.predict(dataset.X_test)

    print(pred)
    report = EvaluationReport(dataset.y_test, pred, dataset.meta.task, target_names=dataset.meta.class_labels)
    print(report.report_str())

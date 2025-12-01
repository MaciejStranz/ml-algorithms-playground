# ml_core/demo.py
from algorithms.ml_models import get_ml_classifier
from data_handlers.load_dataset import load_data
from sklearn.metrics import classification_report

if __name__ == "__main__":
    dataset = load_data("breast_cancer")  

    print("Meta:", dataset.meta)

    model = get_ml_classifier("svm", {"kernel": "linear"})
    model.fit(dataset.X_train, dataset.y_train)
    pred = model.predict(dataset.X_test)

    print(pred)
    report = classification_report(dataset.y_test, pred, target_names=dataset.meta.class_labels)
    print(report)

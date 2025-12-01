from sklearn import svm 

def get_ml_classifier(name: str, params: dict|None = None):
    if name == "svm":
        model = svm.SVC(**params) 
    return model

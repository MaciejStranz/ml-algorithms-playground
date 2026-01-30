from ml_core.algorithms.classical import get_classical_model
from ml_core.data_handlers.load_dataset import load_data
from sklearn.metrics import classification_report
from ml_core.evaluation.metrics import EvaluationReport
from ml_core.algorithms.deep.mlp import get_deep_model
from ml_core.runner import RunConfig, run_experiment

if __name__ == "__main__":
    
    #params = {"kernel": "rbf", "gamma":"scale"}
    params = {}

    RunConf = RunConfig(dataset_name="wine", 
                        algorithm_name="svm",
                        hyperparams=params)
    result = run_experiment(RunConf)
    print(result)

    


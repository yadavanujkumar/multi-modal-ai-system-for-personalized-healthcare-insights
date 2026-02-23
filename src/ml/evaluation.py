# src/ml/evaluation.py

"""
Model evaluation metrics and benchmarking for assessing model performance and identifying areas for improvement.
"""

import logging
from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, f1_score
from sklearn.exceptions import NotFittedError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """
    Evaluates the performance of a machine learning model.
    """

    def __init__(self, model: RandomForestClassifier, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42):
        """
        Initializes the ModelEvaluator.

        Args:
        - model (RandomForestClassifier): The machine learning model to evaluate.
        - X (np.ndarray): The feature data.
        - y (np.ndarray): The target data.
        - test_size (float, optional): The proportion of the data to use for testing. Defaults to 0.2.
        - random_state (int, optional): The random state for reproducibility. Defaults to 42.
        """
        self.model = model
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state

    def split_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Splits the data into training and testing sets.

        Returns:
        - X_train (np.ndarray): The training feature data.
        - X_test (np.ndarray): The testing feature data.
        - y_train (np.ndarray): The training target data.
        - y_test (np.ndarray): The testing target data.
        """
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.test_size, random_state=self.random_state)
        return X_train, X_test, y_train, y_test

    def scale_data(self, X_train: np.ndarray, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Scales the data using StandardScaler.

        Args:
        - X_train (np.ndarray): The training feature data.
        - X_test (np.ndarray): The testing feature data.

        Returns:
        - X_train_scaled (np.ndarray): The scaled training feature data.
        - X_test_scaled (np.ndarray): The scaled testing feature data.
        """
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def evaluate_model(self, X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluates the performance of the model.

        Args:
        - X_train (np.ndarray): The training feature data.
        - X_test (np.ndarray): The testing feature data.
        - y_train (np.ndarray): The training target data.
        - y_test (np.ndarray): The testing target data.

        Returns:
        - metrics (Dict[str, float]): A dictionary containing the evaluation metrics.
        """
        try:
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            matrix = confusion_matrix(y_test, y_pred)
            metrics = {
                "accuracy": accuracy,
                "classification_report": report,
                "confusion_matrix": matrix
            }
            return metrics
        except NotFittedError:
            logger.error("Model not fitted")
            return {}

    def tune_hyperparameters(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, float]:
        """
        Tunes the hyperparameters of the model using GridSearchCV.

        Args:
        - X_train (np.ndarray): The training feature data.
        - y_train (np.ndarray): The training target data.

        Returns:
        - best_params (Dict[str, float]): A dictionary containing the best hyperparameters.
        """
        param_grid = {
            "n_estimators": [10, 50, 100, 200],
            "max_depth": [None, 5, 10, 15]
        }
        scorer = make_scorer(f1_score)
        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring=scorer)
        grid_search.fit(X_train, y_train)
        best_params = grid_search.best_params_
        return best_params

def main():
    # Example usage
    from sklearn.datasets import load_iris
    iris = load_iris()
    X = iris.data
    y = iris.target
    model = RandomForestClassifier()
    evaluator = ModelEvaluator(model, X, y)
    X_train, X_test, y_train, y_test = evaluator.split_data()
    X_train_scaled, X_test_scaled = evaluator.scale_data(X_train, X_test)
    metrics = evaluator.evaluate_model(X_train_scaled, X_test_scaled, y_train, y_test)
    best_params = evaluator.tune_hyperparameters(X_train_scaled, y_train)
    logger.info("Evaluation metrics: %s", metrics)
    logger.info("Best hyperparameters: %s", best_params)

if __name__ == "__main__":
    main()
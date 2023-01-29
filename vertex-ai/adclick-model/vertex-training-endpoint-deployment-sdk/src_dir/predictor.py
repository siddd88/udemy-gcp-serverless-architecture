import numpy as np
from google.cloud.aiplatform.prediction.sklearn.predictor import SklearnPredictor

class AdClickPredictor(SklearnPredictor):

    def __init__(self):
        return

    def load(self, artifacts_uri: str) -> None:
        super().load(artifacts_uri)

    def postprocess(self, prediction_results: np.ndarray) -> dict:
        return {"predictions": [f"{value}" for value in np.round(prediction_results)]}
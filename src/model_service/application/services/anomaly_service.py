import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.exceptions import NotFittedError
from typing import Dict, Any

class AnomalyDetectionService:
    def __init__(self):
        self.models: Dict[str, IsolationForest] = {}

    def _get_or_create_model(self, use_case: str) -> IsolationForest:
        if use_case not in self.models:
            self.models[use_case] = IsolationForest(contamination=0.05, random_state=42)
        return self.models[use_case]

    def detect_anomaly(self, use_case: str, features: Dict[str, float]) -> bool:
        model = self._get_or_create_model(use_case)
        df = pd.DataFrame([features])
        
        try:
            prediction = model.predict(df)
            return prediction[0] == -1
        except NotFittedError:
            model.fit(df)
            return False

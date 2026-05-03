from typing import Dict

import pandas as pd
from prometheus_client import Counter
from sklearn.ensemble import IsolationForest
from sklearn.exceptions import NotFittedError

ANOMALIES_DETECTED = Counter(
    "anomalies_detected_total",
    "Total anomaly detections",
    ["use_case"],
)


class AnomalyDetectionService:
    def __init__(self) -> None:
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
            is_anomaly = bool(prediction[0] == -1)
        except NotFittedError:
            model.fit(df)
            is_anomaly = False

        if is_anomaly:
            ANOMALIES_DETECTED.labels(use_case=use_case).inc()

        return is_anomaly

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class PredictionRequestDTO(BaseModel):
    model_config = ConfigDict(extra="allow")
    features: Dict[str, Any]


class PredictionResponseDTO(BaseModel):
    use_case: str
    prediction: Any
    model_version: str
    is_anomaly: bool = False


class IngestionDTO(BaseModel):
    features: Dict[str, Any]
    target: Any = None

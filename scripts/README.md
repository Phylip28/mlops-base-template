# Scripts del Proyecto

Este directorio contiene scripts operativos para ejecucion local del flujo MLOps.

## Flujo base (fase 0)
- generate_data.py: genera datasets sinteticos en data/raw.
- train_dummy.py: entrena modelo base y registra metricas/modelo en MLflow.

## Flujo streaming (fase 1)
- e2e_demo_mlflow.py: envia una rafaga de ingesta para forzar retraining y validar MLflow.
- simulate_multi_streaming.py: simula trafico continuo multi-tenant por use_case.

## Orden recomendado de uso
1. docker-compose up -d
2. python scripts/generate_data.py
3. python scripts/train_dummy.py
4. Levantar API
5. python scripts/e2e_demo_mlflow.py o python scripts/simulate_multi_streaming.py

## Politica de mantenimiento
- Mantener aqui solo scripts reutilizables y seguros para ejecucion manual.
- Evitar scripts que sobreescriban codigo fuente del proyecto.

# Guia MLOps: Plataforma Multi-tenant (Streaming y AutoML)

Esta guia resume la operacion de la fase de streaming en el estado actual del codigo.

## Resumen funcional
1. Rutas dinamicas por caso de uso: `/predict/{use_case}` y `/ingest/{use_case}`.
2. Deteccion de anomalias por use_case con `IsolationForest`.
3. Ingesta en background para no bloquear respuestas HTTP.
4. Reentrenamiento automatico cuando el lote llega al umbral configurado.

## Detalles clave del runtime actual
- El orquestador escribe datos en `data/raw/streaming/{use_case}/data.csv`.
- El umbral de reentrenamiento es `30` muestras (modo demostracion).
- Al reentrenar, registra metricas y modelo en MLflow.
- El modelo se publica como `{use_case}_model` y se asigna alias `champion`.
- Despues del entrenamiento, el CSV usado se archiva como `data_archived_<run_id>.csv`.

## Como probarlo

### 1) Levantar infraestructura
```bash
docker-compose up -d
```

### 2) Levantar la API desde la raiz del repo
```bash
uvicorn src.model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000
```

### 3) Simular trafico streaming
```bash
python scripts/simulate_multi_streaming.py
```

Opcional para forzar entrenamiento rapido:

```bash
python scripts/e2e_demo_mlflow.py
```

## Que deberias observar
1. Se crean carpetas por use_case en `data/raw/streaming/`.
2. El endpoint de ingesta responde rapido mientras escribe en background.
3. Al alcanzar el umbral, aparece log de reentrenamiento en la consola de la API.
4. En MLflow (`http://localhost:5000`) aparecen nuevas corridas y versiones de modelo.

## Riesgos comunes
- `run_platform.py` usa PowerShell y no es portable tal cual a bash.
- El proyecto asume credenciales locales para MinIO/MLflow en entorno de desarrollo.
- Ejecuta comandos desde la raiz del repositorio para evitar rutas relativas rotas.

# Comandos Rapidos

## Flujo completo (PowerShell/Windows)
```bash
python run_platform.py
```

## Prueba E2E corta (fuerza entrenamiento)
```bash
python scripts/e2e_demo_mlflow.py
```

## Simulacion de streaming
```bash
python scripts/simulate_multi_streaming.py
```

## Calidad de codigo
```bash
pytest tests/
ruff check src/
ruff format src/
mypy src/
```
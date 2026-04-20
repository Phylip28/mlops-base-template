# ?? Guía MLOps: Plataforma Multi-Tenant (Streaming & AutoML)

Esta actualización transforma la plantilla en un sistema **Multi-Caso de Uso**, permitiendo ingesta continua (streaming) y reentrenamiento automático en caliente (AutoML) sobre la misma infraestructura base.

## ?? Características Añadidas
1. **Rutas Dinámicas ({use_case})**: Sirven de identificador principal para aislamiento de datos.
2. **Detección de Data Drift (Anomaly Service)**: Uso de _Isolation Forest_ no supervisado para chequear outliears en los datos entrantes.
3. **Ingesta Continua (Background Tasks)**: Guardado on-the-fly (ppend) usando BackgroundTasks de FastAPI para no generar latencia al cliente.
4. **Política de Auto-Retraining**: Cuando un caso de uso acumula suficientes datos nuevos (N=50 para propósitos demostrativos), se dispara un ciclo offline de entrenamiento y se registra la métrica con el tracking URI dinámico (\sqlite:///mlflow.db\).

---

## ?? Cómo Ponerlo A Prueba

### 1. Iniciar la API de FastAPI
En una terminal (consola), colócate en la raíz del proyecto y levanta el servidor (que ahora actúa a su vez como receptor de streaming y orquestador local):
\\\powershell
cd src
\="."
uvicorn model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000 --reload
\\\

### 2. Ejecutar el Simulador de Tráfico (Ingesta Streaming)
Abre **otra** terminal en la raíz de tu proyecto actívala (\.venv\\Scripts\\Activate.ps1\) y lanza el script de simulación:
\\\powershell
python scripts/simulate_multi_streaming.py
\\\

#### ¿Qué observarás durante la ejecución?
1. **Terminal 2 (Simulador):** Verás cómo los sistemas reportan "ingestas" divididas entre \raude_financiero\ y \bandono_clientes\. Los primeros registros pueden mostrarse como anómalos \[Anomaly]\ debido al arranque del Isolation Forest, hasta que recopila suficiente información histórica.
2. **Terminal 1 (Servidor API):** 
   - Apenas la cola de guardado alcanza **50 elementos** para un \use_case\ específico, verás este log saltar desde la tarea en Background:
   > [MLOps] Reentrenando <caso_uso> con 50 samples...
   - Luego verás que el archivo crudo de \data.csv\ respectivo se archiva automáticamente (data_archived.csv) para repetir el ciclo de monitoreo sobre datos frescos.

### 3. Comprobar que los Datos se Separaron (Particionamiento)
Navega a la carpeta \data/raw/streaming/\. Encontrarás que el sistema creó dinámicamente dos carpetas hijas (una por cada caso de uso), conteniendo sus respectivos features guardados de manera independiente.

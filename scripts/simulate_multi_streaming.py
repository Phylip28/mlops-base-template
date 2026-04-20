import time
import random
import requests
import json

API_URL = "http://localhost:8000"

USE_CASES = {
    "fraude_financiero": {
        "features": ["monto", "distancia_km", "hora_transaccion"],
        "target_prob": 0.05
    },
    "abandono_clientes": {
        "features": ["dias_inactivo", "tickets_soporte", "gasto_mensual"],
        "target_prob": 0.15
    }
}

def generate_random_payload(use_case_name: str) -> dict:
    meta = USE_CASES[use_case_name]
    features = {}
    for feat in meta["features"]:
        features[feat] = round(random.uniform(0.1, 1000.0), 2)
    target = 1 if random.random() < meta["target_prob"] else 0
    return {"features": features, "target": target}

def simulate_streaming(num_events: int = 150):
    print("Iniciando Simulador de Ingesta MLOps - {} eventos...".format(num_events))
    
    for i in range(1, num_events + 1):
        use_case = random.choice(list(USE_CASES.keys()))
        payload = generate_random_payload(use_case)
        
        try:
            res_ingest = requests.post(f"{API_URL}/ingest/{use_case}", json=payload)
            anomaly_flag = res_ingest.json().get('anomaly_flagged', False)
            anomaly_str = "Anomaly" if anomaly_flag else "Normal"
            
            pred_payload = {"features": payload["features"]}
            requests.post(f"{API_URL}/predict/{use_case}", json=pred_payload)
            
            print(f"[{i:03d}] {anomaly_str} Ingestado -> {use_case}")
        except requests.exceptions.RequestException as e:
            print(f"[{i:03d}] Error de conexion al servidor: {e}")
            
        time.sleep(0.05)
        
    print("Simulacion completada!")

if __name__ == "__main__":
    simulate_streaming()

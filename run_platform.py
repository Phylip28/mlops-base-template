import os
import shutil
import subprocess
import sys
import time
import webbrowser
import psutil

def _resolve_docker_compose() -> list[str]:
    if shutil.which('docker-compose'):
        return ['docker-compose']
    if shutil.which('docker'):
        return ['docker', 'compose']
    raise RuntimeError('No se encontro Docker Compose.')

def start_api() -> subprocess.Popen:
    print('[API] Iniciando Uvicorn (FastAPI) en background...', flush=True)
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'
    venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        venv_python = sys.executable
    cmd = [
        venv_python,
        '-m',
        'uvicorn',
        'src.model_service.infrastructure.entrypoints.api:app',
        '--host',
        '0.0.0.0',
        '--port',
        '8000',
    ]
    return subprocess.Popen(cmd, env=env)

def main() -> None:
    print('====================================')
    print('=== MLOps Platform Runner (E2E)  ===')
    print('====================================')

    print('\n[1/3] Levantando infraestructura (MLflow, MinIO, Postgres, Prometheus, Grafana)...')
    try:
        compose_cmd = _resolve_docker_compose()
        subprocess.run(compose_cmd + ['up', '-d'], check=True)
    except Exception as err:
        print(f'Error levantando Docker Compose: {err}')
        sys.exit(1)

    print('\n[2/3] Levantando la API REST Server en puerto 8000...')
    try:
        api_process = start_api()
        time.sleep(5) # Wait for it to boot
    except Exception as err:
        print(f'Error iniciando API: {err}')
        sys.exit(1)

    print('\n[3/3] Levantando Interfaz Grafica de Control Visual (Streamlit)...')
    venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
    
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    cmd = [venv_python, '-m', 'streamlit', 'run', 'run_streamlit_app.py', '--server.port', '8502']
    
    print('\n🚀 Servicios en linea!')
    print('------------------------------------------------')
    print('El Centro de Control se abrira en tu navegador automaticamente.')
    print('URL: http://localhost:8502')
    print('------------------------------------------------')
    try:
        webbrowser.open('http://localhost:8502')
    except Exception:
        pass
    
    try:
        print('Presiona CTRL+C en esta terminal para apagar el ecosistema...')
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print('\n\nCentro de control detenido.')
        print('Apagando Uvicorn si estaba abierto...')
        if api_process.poll() is None:
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                api_process.kill()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline') or []
                if 'uvicorn' in ' '.join(cmdline):
                    proc.kill()
            except Exception:
                pass
        print('Ejecutando docker-compose down...')
        try:
            subprocess.run(compose_cmd + ['down'], check=False)
        except:
             pass
        print('Contenedores detenidos.')
        sys.exit(0)

if __name__ == '__main__':
    main()
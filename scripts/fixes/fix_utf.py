import shutil
import codecs

src = 'scripts/e2e_demo_mlflow.py'
with open(src, 'rb') as f:
    text = f.read().decode('utf-16' if f.read(2) == b'\xff\xfe' else 'utf-8', errors='ignore')

with open(src, 'w', encoding='utf-8') as f:
    f.write(text)

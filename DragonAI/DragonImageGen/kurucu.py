import os
import subprocess

def setup():
    # 1. Önce sanal ortamı oluşturur
    if not os.path.exists("venv"):
        subprocess.run("python -m venv venv", shell=True)

    # 2. AKTİVASYONLA UĞRAŞMAZ, yolu direkt gösterir:
    pip_path = os.path.join("venv", "Scripts", "pip.exe")
    python_path = os.path.join("venv", "Scripts", "python.exe")

    # 3. Bu yollar üzerinden her şeyi kurar
    subprocess.run(f"{pip_path} install ...", shell=True)

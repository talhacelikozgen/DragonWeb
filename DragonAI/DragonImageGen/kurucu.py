import os
import subprocess

def setup():
    # 1. Sanal ortam yoksa oluştur
    if not os.path.exists("venv"):
        print("Sanal ortam olusturuluyor...")
        subprocess.run("python -m venv venv", shell=True)

    # 2. Yolları belirle (Windows için .exe ekliyoruz)
    pip_path = os.path.join("venv", "Scripts", "pip.exe")
    python_path = os.path.join("venv", "Scripts", "python.exe")

    # 3. Kütüphaneleri venv içine kur
    print("Kutuphaneler yukleniyor, bu biraz zaman alabilir...")
    
    # Önce temel kütüphaneler ve Intel optimizasyonlu Torch
    subprocess.run(f"{pip_path} install --upgrade pip", shell=True)
    subprocess.run(f"{pip_path} install torch torchvision --index-url https://download.pytorch.org/whl/cpu", shell=True)
    
    # Intel Extension for PyTorch (Intel Arc için hayati olan kısım)
    subprocess.run(f"{pip_path} install intel-extension-for-pytorch==2.1.10+xpu --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/", shell=True)
    
    # Diğer gerekli kütüphaneler
    subprocess.run(f"{pip_path} install diffusers transformers accelerate safetensors huggingface_hub fastapi uvicorn", shell=True)

    print("Kurulum tamamlandi!")

if __name__ == "__main__":
    setup()

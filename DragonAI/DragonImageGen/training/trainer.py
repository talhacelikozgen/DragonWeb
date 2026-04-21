import torch
import intel_extension_for_pytorch as ipex
from diffusers import DiffusionPipeline
from peft import LoraConfig, get_peft_model
import os

class DragonTrainer:
    def __init__(self, base_model="runwayml/stable-diffusion-v1-5"):
        self.device = "xpu"
        self.base_model = base_model
        
    def setup_lora(self):
        # LoRA Konfigürasyonu: VRAM dostu öğrenme
        config = LoraConfig(
            r=16, # Öğrenme kapasitesi
            lora_alpha=32,
            target_modules=["to_q", "to_v"], # Dikkat (Attention) katmanlarını eğitir
            lora_dropout=0.05,
            bias="none"
        )
        return config

    def start_training(self, dataset_path, output_name="dragon_style_v1"):
        print(f"--- Dragon AI Öğrenme Süreci Başladı: {output_name} ---")
        
        # Modeli yükle ve IPEX ile optimize et
        model = DiffusionPipeline.from_pretrained(self.base_model).to(self.device)
        lora_config = self.setup_lora()
        
        # XMX Hızlandırma ve BF16 (Bfloat16) hassasiyeti ile bellek yönetimi
        model.unet = ipex.optimize(model.unet, dtype=torch.bfloat16)
        
        # Burada eğitim döngüsü (loop) başlar...
        # Veri gizliliği için tüm checkpoint'ler yerel diske kaydedilir.
        save_path = f"./lora_weights/{output_name}"
        os.makedirs(save_path, exist_ok=True)
        print(f"Öğrenilen veriler kaydediliyor: {save_path}")

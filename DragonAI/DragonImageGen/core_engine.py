import torch
import intel_extension_for_pytorch as ipex # XMX Hızlandırma için kritik
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from pathlib import Path

class DragonEngine:
    def __init__(self, model_path="./models/stable-diffusion-v1-5"):
        self.device = "xpu" # Intel GPU kullanımı
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        # Offline Model Yönetimi ve Safetensors yükleme
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_path, 
            torch_dtype=torch.float16, # VRAM Tasarrufu
            use_safetensors=True
        )
        
        # Intel Arc XMX Hızlandırması ve IPEX Optimizasyonu
        self.pipe = self.pipe.to(self.device)
        self.pipe.unet = ipex.optimize(self.pipe.unet, dtype=torch.float16)
        
        # Inference Steps Optimizasyonu için Scheduler
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)

    def generate(self, prompt, neg_prompt, steps=25, scale=7.5):
        # Latent Diffusion ve VAE kontrolü burada gerçekleşir
        with torch.xpu.amp.autocast(): # Otomatik Karışık Hassasiyet
            image = self.pipe(
                prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=steps,
                guidance_scale=scale
            ).images[0]
        return image

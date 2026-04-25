import torch
import intel_extension_for_pytorch as ipex 
# Pylance'in istediği tam yol (import yolu değişti):
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
import os

class DragonEngine:
    def __init__(self):
        print("--- Dragon AI Motoru Başlatılıyor (Intel Arc B580) ---")
        
        # Model yolu (Klasörde bu ismin birebir aynı olduğundan emin ol!)
        self.model_path = "./models/realisticVisionV60_v60B1.safetensors"
        self.device = "xpu"  

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model dosyasi bulunamadi: {self.model_path}. Lutfen 'models' klasorunu kontrol edin.")

        # 1. Modeli Yükle
        self.pipe = StableDiffusionPipeline.from_single_file(
            self.model_path, 
            torch_dtype=torch.float16, 
            safetensors=True
        )

        # 2. Intel Arc Optimizasyonlarını Uygula
        self.pipe = self.pipe.to(self.device)
        
        # IPEX ile katmanları optimize et
        self.pipe.unet = ipex.optimize(self.pipe.unet, dtype=torch.float16)
        self.pipe.vae = ipex.optimize(self.pipe.vae, dtype=torch.float16)
        self.pipe.text_encoder = ipex.optimize(self.pipe.text_encoder, dtype=torch.float16)
        
        print("--- Dragon AI Motoru Hazır! ---")

    def generate(self, prompt: str, negative_prompt: str, steps: int):
        # Intel Karışık Hassasiyet (AMP) kullanarak görsel üret
        # 'with torch.xpu.amp.autocast()' Intel Arc için bellek ve hız dengesini sağlar
        with torch.xpu.amp.autocast(), torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=7.5
            )
            
            # // işaretini sildik, Python listesinden ilk resmi çekiyoruz
            image = result.images[0]
        
        return image
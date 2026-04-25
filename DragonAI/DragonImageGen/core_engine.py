import os
import torch
import time

# IPEX hatasını engellemek için ortam değişkenlerini temizleyelim
os.environ["PYTORCH_ENABLE_XPU_FALLBACK"] = "1"

class DragonEngine:
    def __init__(self):
        print("--- Dragon AI Motoru Başlatılıyor (Direct XPU Mode) ---")
        
        # Cihazı XPU (Intel GPU) olarak belirliyoruz
        self.device = "xpu" 
        self.model_id = "runwayml/stable-diffusion-v1-5"
        
        from diffusers import StableDiffusionPipeline
        
        try:
            print(f"Model {self.device} üzerine yükleniyor...")
            # IPEX'i import etmiyoruz, direkt PyTorch üzerinden yüklüyoruz
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, 
                torch_dtype=torch.float16,
                use_safetensors=True
            ).to(self.device)
            
            print("--- Dragon AI Motoru Hazır! ---")
        except Exception as e:
            print(f"--- [KRİTİK HATA] GPU Modu Başarısız: {e} ---")
            print("İpucu: Eğer hala hata alıyorsanız Intel Arc sürücülerinizi güncelleyin.")

    def generate(self, prompt, negative_prompt="", steps=20, width=512, height=512):
        print(f"Üretim Başladı: {prompt}")
        
        # Üretim işlemi (IPEX optimizasyonu olmadan, saf PyTorch hızıyla)
        image = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=7.5,
            width=width,
            height=height
        ).images[0]
        
        # Kayıt
        timestamp = int(time.time())
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, f"dragon_{timestamp}.png")
        image.save(output_path)
        print(f"Görsel başarıyla kaydedildi: {output_path}")
        return output_path
from fastapi import FastAPI

from pydantic import BaseModel

from core_engine import DragonEngine

import os



app = FastAPI(title="Dragon AI Local API")

engine = DragonEngine()



class ImageRequest(BaseModel):

    prompt: str

    negative_prompt: str = "low quality, blurry, distorted"

    steps: int = 20



@app.post("/generate")

async def process_image(request: ImageRequest):

    # Veri Gizliliği: Görsel sadece yerel depolamaya kaydedilir

    image = engine.generate(request.prompt, request.negative_prompt, request.steps)

    save_path = f"outputs/{os.urandom(4).hex()}.png"

    image.save(save_path)

    return {"status": "success", "path": save_path}
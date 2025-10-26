from src.db.dbHandler import add_feedback, add_generated_content
from omegaconf import OmegaConf
# from src.models.txt_model import generate_hashtags
# from src.models.fig_model import generate_image

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel




cfg = OmegaConf.load("src/configs/configs.yaml")

class Prompt(BaseModel):
    description: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hashtag and Image Generation API!"}


@app.post("/generate/")
async def generate_content(prompt: Prompt):
    description = prompt.description
    try:
        hashtags = generate_hashtags(description, cfg)
        img = generate_image(description, cfg)


        return {
            "hashtags": hashtags,
            "image_url": image_url
        }
        add_feedback(description, hashtags, image_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Generation failed")






from src.db.dbHandler import add_feedback, add_generated_content
from omegaconf import OmegaConf
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

cfg = OmegaConf.load("src/configs/configs.yaml")



class Prompt(BaseModel):
    description: str


app = FastAPI()


@app.get("/")
def read_root():
    """
    Returns a welcome message for the root path of the API.
    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to the Hashtag and Image Generation API!"}


@app.post("/generate/")
async def generate_content(prompt: Prompt):
    """
    Generates an image and hashtags based on the given description.
    Args:
        prompt (Prompt): A dictionary containing a description.
    Returns:
        dict: A dictionary containing the generated hashtags and image url.
    Raises:
        HTTPException: If the generation failed.
    """
    description = prompt.description
    try:
        hashtags = generate_hashtags(description, cfg)
        # img = generate_image(description, cfg)
        os.makedirs("src/db/static/generated", exist_ok=True)
        # add generated content to the database and get the id
        id = add_generated_content(description, hashtags)
        # save the image with the id as filename
        image_url = f"src/db/static/generated/{id}.png"
        # img.save(image_url)
        return {
            "hashtags": hashtags,
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Generation failed")


@app.post("/train")
def train_models(background_tasks: BackgroundTasks):
    background_tasks.add_task(train_model, "text_model")
    background_tasks.add_task(train_model, "fig_model")
    return {"message": "Training started in the background"}


@app.post("/add_feedback")
def store_feedback(id: int, user_feedback: int):
    return add_feedback(id, user_feedback)
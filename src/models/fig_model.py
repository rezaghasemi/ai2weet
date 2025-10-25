import os
import torch
from diffusers import StableDiffusionPipeline
from omegaconf import OmegaConf
from src.utiles.getDevice import getDevice

# Load config
cfg = OmegaConf.load("src/configs/configs.yaml")

model_name = cfg.fig_model.name
models_path = cfg.fig_model.models_path
local_dir = f"{models_path}/{model_name}"  # customize as you like

# Check if model already exists locally
if not os.path.exists(local_dir):
    print(f"Downloading {model_name} and saving to {local_dir}...")
    pipe = StableDiffusionPipeline.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
    )
    os.makedirs(local_dir, exist_ok=True)
    pipe.save_pretrained(local_dir)
else:
    print(f"Loading {model_name} from {local_dir}...")

# Load the pipeline from the local directory
fig_llm = StableDiffusionPipeline.from_pretrained(
    local_dir,
    torch_dtype=torch.float16,
)

# Move to correct device
fig_llm.to(getDevice())

def generate_image(prompt: str):
    prompt = cfg.fig_prompts.prefix + prompt
    image = fig_llm(prompt,
                    num_inference_steps=cfg.fig_model.generation_params.num_inference_steps,
                    guidance_scale=cfg.fig_model.generation_params.guidance_scale).images[0]
    return image
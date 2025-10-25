import os
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from omegaconf import OmegaConf

# Load config
cfg = OmegaConf.load("src/configs/configs.yaml")

model_name = cfg.txt_model.name
models_path = cfg.txt_model.models_path

local_dir = f"{models_path}/{model_name}"  # you can change this path

# Check if model already exists locally
if not os.path.exists(local_dir):
    print(f"Downloading {model_name} and saving to {local_dir}...")
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    os.makedirs(local_dir, exist_ok=True)
    model.save_pretrained(local_dir)
    tokenizer.save_pretrained(local_dir)
else:
    print(f"Loading {model_name} from {local_dir}...")

# Load pipeline
hashtag_llm = pipeline(
    task="text-generation",
    model=local_dir,
    torch_dtype=torch.float16,
    device=0
)


def generate_hashtags(prompt: str):
    prompt = cfg.txt_prompts.prefix + prompt
    return hashtag_llm(prompt, 
                       max_new_tokens=cfg.txt_model.generation_params.max_new_tokens, 
                       do_sample=cfg.txt_model.generation_params.do_sample,
                       top_k=cfg.txt_model.generation_params.top_k,
                       top_p=cfg.txt_model.generation_params.top_p,
                       temperature=cfg.txt_model.generation_params.temperature)[0]['generated_text']
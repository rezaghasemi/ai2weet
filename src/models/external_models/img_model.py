from dotenv import load_dotenv
from omegaconf import OmegaConf

cfg = OmegaConf.load("src/configs/configs.yaml")
api_key_file = load_dotenv(cfg.models.img_external_model.api_key_path)
API_KEY = api_key_file.get("OPENAI_API_KEY")



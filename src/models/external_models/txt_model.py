from dotenv import load_dotenv
from omegaconf import OmegaConf
from typing import List

import os

cfg = OmegaConf.load("src/configs/configs.yaml")
load_dotenv(dotenv_path=cfg.txt_external_model.api_key_path)
prefix_prompt = cfg.txt_prompts.prefix



if cfg.txt_external_model.name == "OPENAI":
    from openai import OpenAI, OpenAIError, APIError, APIConnectionError, RateLimitError, AuthenticationError
    API_KEY = os.environ.get("OPENAI_API_KEY")
    MODEL_NAME = cfg.txt_external_model.name
    client = OpenAI(api_key=API_KEY)
else:
    raise ValueError("Unsupported external model specified in configuration.")

def generate_hashtags(prompt: str) -> str:
    if MODEL_NAME == "OPENAI":
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates hashtags for social media posts."},
                    {"role": "user", "content": prefix_prompt + prompt}
                ],
                max_tokens=10,
                n=1,
                stop=None,
                temperature=0.7,
            )
            hashtags = response.choices[0].message.content.strip()
        
        except AuthenticationError:
            print("❌ Invalid API key. Please check your credentials.")

        except RateLimitError:
            print("⚠️ You hit the rate limit. Try again later.")

        except APIConnectionError:
            print("🌐 Network issue. Please check your internet connection.")

        except APIError as e:
            print(f"⚙️ API error: {e}")

        except OpenAIError as e:
            print(f"Something unexpected happened: {e}")
                
        return hashtags
    

def cleanup(response: str) -> List[str]:
    cleaned_response = [tag[1:] if tag.startswith('#') else tag for tag in response.split()]
    return cleaned_response
    
if __name__ == "__main__":
    test_prompt = "Exploring the beautiful landscapes of New Zealand!"
    print(cleanup(generate_hashtags(test_prompt)))
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.environ['ARTIST_API_KEY']
model = os.environ['ARTIST_MODEL']
base_url = os.environ['ARTIST_URL']

client = OpenAI(api_key=api_key,
                base_url="https://api.together.xyz/v1",)



def get_image(prompt: str):
    """Fetch an image based on the prompt."""
    try:
      img = client.images.generate(
          model=model,
          prompt=prompt,
      )
      if img and img.data and len(img.data) > 0:
          if img.data[0].b64_json:
              return base64.b64decode(img.data[0].b64_json)
          elif img.data[0].url:
              return img.data[0].url
      return "assets/placeholder.png"
    except Exception as e:
      print(f"Error fetching image: {e}")
      return "assets/placeholder.png"
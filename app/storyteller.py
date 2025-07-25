import os
import json
from openai import OpenAI
from constants import storyteller_prompt, story_image_description_prompt
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_key  = os.environ['STORYTELLER_API_KEY']
base_url  = os.environ['STORYTELLER_URL']
model = os.environ['STORYTELLER_MODEL']

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


def generate_story(genres: list[str], custom_characters: str, num_paragraphs: int) -> dict[str, str]:
  response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": storyteller_prompt},
        {"role": "user", "content": f"### Genres: {', '.join(genres)}.\nCharacters: {custom_characters}\nNumber of paragraphs: {num_paragraphs}."}
    ]
  )
  content: str = "" + (response.choices[0].message.content or "")
  content = content.removeprefix('```json\n').removesuffix('\n```')
  json_content = json.loads(content)
  return json_content

def generate_image_description(paragraph: str) -> dict[str, str]:
  """Generate a description for the image based on the paragraph content."""
  response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": story_image_description_prompt},
        {"role": "user", "content": f"### {paragraph}"}
    ]
  )
  content: str = "" + (response.choices[0].message.content or "")
  content = content.removeprefix('```json\n').removesuffix('\n```')
  json_content = json.loads(content)
  return json_content
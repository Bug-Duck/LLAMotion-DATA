import json
import os
from openai import OpenAI
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

with open("src/file.json", "r") as f:
  file_id = json.loads(f.read())["file_id"]

client.fine_tuning.jobs.create(
  training_file=file_id,
  model="gpt-4o-mini-2024-07-18"
)
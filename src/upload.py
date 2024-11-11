from openai import OpenAI
import json
import os

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

file = client.files.create(
  file=open("training_data.jsonl", "rb"),
  purpose="fine-tune"
)

with open("file.json", "w") as f:
  f.write(str(file))

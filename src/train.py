import os
from openai import OpenAI
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

client.fine_tuning.jobs.create(
  training_file="file-ALtFvAFQ0oQ5PJNAoBkrn06q",
  model="gpt-4o-mini-2024-07-18"
)
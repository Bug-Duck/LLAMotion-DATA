import os
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

jobs = client.fine_tuning.jobs.list()

print(jobs)
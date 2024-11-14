import os
import json
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

jobs = client.fine_tuning.jobs.list()

with open("src/jobs.json", "w") as f:
  f.write(json.dumps({
    "job_id": jobs.data[0].id,
    "model": jobs.data[0].fine_tuned_model
  }))
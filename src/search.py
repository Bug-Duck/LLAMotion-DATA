import os
import json
from openai import OpenAI
from time import sleep
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

def main(index):
  with open("src/jobs.json", "r") as f:
    jobs = json.loads(f.read())

  events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=jobs["job_id"], limit=10)
  print(str(index) + " " + str(events.data[0].message))

if __name__ == "__main__":
  index = 0
  while True:
    main(index)
    index += 1
    sleep(1)

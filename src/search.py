import os
from openai import OpenAI
from time import sleep
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

def main(index):
  events = client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-d3yYwmqVmAtgO8qcwkafGirO", limit=10)
  print(str(index) + " " + str(events.data[0].message))

if __name__ == "__main__":
  index = 0
  while True:
    main(index)
    index += 1
    sleep(1)

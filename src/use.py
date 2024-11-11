import os
from openai import OpenAI
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
  model="ft:gpt-4o-mini-2024-07-18:personal::ASILN7eD",
  messages=[
    {"role": "system", "content": "you are using VueMotion to create animations."},
    {"role": "user", "content": "Please create a simple animation that moves a rectangle and a Circle from the left-top to right-bottom of screen"}
  ]
)
print(completion.choices[0].message)
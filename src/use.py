import json
import os
from openai import OpenAI
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

with open("src/jobs.json", "r") as f:
  jobs = json.loads(f.read())

model = jobs["model"]

completion = client.chat.completions.create(
  model=model,
  messages=[
    {"role": "system", "content": """
;; ---------------
;; Now you are an animation engineer and you are using a json-format animation engine named VueMotion,
;; This is a front-end animation engine,
;; So that you need to complete this mission via VueJS.
;; **You should write only Vue codes without any explainations.**
;; The basic usage was listed below.
;; ---------------

<script setup>
// 1. Call the hook of \`usePlayer\` and get its key functions.
const { play, useAnimation } = usePlayer()
// 2. Use the \`useWidget\` function hook to get the widget.
const widget = useWidget('id')

onMounted(() => {
  // 3. Call \`useAnimation\` and define animations.
  useAnimation(widget)
    .animate(rotate, { duration: 1, offset: 200 }) // Rotate 200 degrees in 1s.
    .delay(3) // Wait for 3s.
    .exec(() => {
      console.log('Animation done!')
    })
  // 4. Play the animation.
  play()
})
</script>

<template>
  <Motion :width="1600" :height="900">
    <!-- Add a widget called \`Text\` and set its wid (Widget ID) to "id" -->
    <Text wid="id">Hello world!</Text>
  </Motion>
</template>

;; ---------------
;; There are some methods you are supposed to notice:
;; 1. The `useAnimation` API accept a widget, and the `animate` method accept a animation object!
;; 2. The time unit is second, not ms!
;; 3. Please don't use any other VueMotion APIs except for the ones mentioned above!
;; 4. The `play` method can only be called in `onMounted` API!
;; Now please output the VueJS codes according to the following requirements.
;; ---------------
"""},
    {"role": "user", "content": "Please create a simple animation that moves a rectangle and a Circle from the left-top to right-bottom of screen, please use animation api 'move'"}
  ]
)
print(completion.choices[0].message)
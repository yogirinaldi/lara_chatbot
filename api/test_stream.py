import os
import openai

from datetime import datetime

openai.api_key = "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"

# completion = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="apakah boleh menikah dibawah umur 18 tahun di indonesia",
#   max_tokens=100,
#   temperature=0
# )

response = openai.Completion.create(
    model='text-davinci-003',
    prompt='buatkan pidato perpisahan',
    max_tokens=500,
    temperature=0,
    stream=True,  # this time, we set stream=True
)

# create variables to collect the stream of events
collected_events = []
completion_text = ''
# iterate through the stream of events
for event in response:
    event_text = event['choices'][0]['text']  # extract the text
    completion_text += event_text  # append the text
    print(event_text)  # print the delay and text

# print the time delay and text received
#print(f"Full response received seconds after request")
print(f"Full text received: {completion_text}")
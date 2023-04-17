# After finishing fine-tune, test fine-tune model

import asana
import openai
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Asana API key
ASANA_API_KEY = os.getenv('ASANA_API_KEY')
asana_client = asana.Client.access_token(ASANA_API_KEY)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def get_asana_task(task_gid):
    client = asana.Client.access_token(ASANA_API_KEY)
    client.headers.update({
        "Asana-Enable": "new_user_task_lists,new_goal_memberships"
    })
    task = client.tasks.get_task(task_gid)
    return task

task_gid = '' # Replace with the task ID you want to process
task = get_asana_task(task_gid)
# Check if '描述' is present in task['notes']
if '描述' in task['notes']:
    defect_description = task['notes']
else: # If not, get task name as defect description
    defect_description = task['name']
prompt = f"將以下描述轉為test case: {defect_description} "

# Use your fine-tuned model
model_name = "davinci:ft-personal-2023-04-16-12-09-03" # Replace with the your fine-tune model ID

response = openai.Completion.create(
    model=model_name,
    prompt=prompt,
    max_tokens=500,
    temperature=0.8,
)

test_steps = response.choices[0].text.strip()
print(test_steps)
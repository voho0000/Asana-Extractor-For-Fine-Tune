import asana
import os
import requests
import json
import re
from dotenv import load_dotenv

# Set up Asana API key
ASANA_API_KEY = os.getenv('ASANA_API_KEY')

# Each defect description and corresponding test case will be stored in defects folder
import asana
import os
import json
import re

def get_asana_task(task_gid):
    client = asana.Client.access_token(ASANA_API_KEY)
    client.headers.update({
        "Asana-Enable": "new_user_task_lists,new_goal_memberships"
    })
    task = client.tasks.get_task(task_gid, opt_fields=["custom_fields", "notes", "name"])
    return task

# Function to extract custom fields
def extract_custom_fields(task):
    custom_fields = {
        "Pre-Condition": "",
        "Test Step": "",
        "Expected Result": "",
        "Additional Step": "",
        "MainTicket": None
    }

    for field in task["custom_fields"]:
        field_name = field["name"]
        field_value = field.get("text_value", "")
        if field_name in custom_fields:
            custom_fields[field_name] = field_value

    return custom_fields

# Function to extract task ID from the URL
def extract_task_id_from_url(url):
    task_id_pattern = r"/(\d+)(/f)?$"
    match = re.search(task_id_pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Create the 'defects' directory if it doesn't exist
if not os.path.exists('defects'):
    os.makedirs('defects')

# List of Asana task IDs
task_ids = [
    
]  # **Replace with your actual list of Asana task IDs**

# Iterate through the task IDs and create individual JSON files
for i, task_id in enumerate(task_ids, start=2):
    task = get_asana_task(task_id)
    extracted_fields = extract_custom_fields(task)
    # get "test steps" from "Pre-Condition", "Test Step", "Expected Result", "Additional Step"
    desired_keys = ["Pre-Condition", "Test Step", "Expected Result", "Additional Step"]
    new_fields = {key: extracted_fields[key] for key in desired_keys}
    test_steps = new_fields

    # Fetch the corresponding test case ticket and get the test steps
    main_ticket_url = extracted_fields["MainTicket"]
    if main_ticket_url:
        main_ticket_gid = extract_task_id_from_url(main_ticket_url)
        main_ticket_task = get_asana_task(main_ticket_gid)
        # Check if '描述' is present in main_ticket_task['notes']
        if '描述' in main_ticket_task['notes']:
            defect_description = main_ticket_task['notes']
        else: # If not, get task name as defect description
            defect_description = main_ticket_task['name']
    else:
        raise ValueError(f"No MainTicket URL found for task with ID {task_id}")


    # Create the JSON file
    data = {
        "defect_description": defect_description,
        "test_steps": test_steps
    }

    file_name = f'defect_{main_ticket_gid}.json'
    file_path = os.path.join('defects', file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Create training data file from the 'defects' folder
defect_folder = "defects"
files = [f for f in os.listdir(defect_folder) if f.endswith(".json")]
# We need to add stop token for prompt and completion. Stop token should not appear in the prompt or completion.
prompt_template = "產生test case：[defect_description_1] <|sep|>" 
completion_template = " [test_steps_1] <|stop|>"

dataset = []

for file in files:
    with open(os.path.join(defect_folder, file), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entry = {
        "prompt": prompt_template.replace("[defect_description_1]", data["defect_description"]),
        "completion": completion_template.replace("[test_steps_1]", json.dumps(data["test_steps"], ensure_ascii=False))
    }
    
    dataset.append(entry)

print(dataset)

# Save the dataset to a JSONL file
with open('training_data.jsonl', 'w', encoding='utf-8') as outfile:
    for entry in dataset:
        json.dump(entry, outfile, ensure_ascii=False)
        outfile.write('\n')
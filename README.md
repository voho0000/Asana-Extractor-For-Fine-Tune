# Asana Test Case Extractor for GPT fine tune
Asana Test Case Extractor is a Python script that extracts test cases from Asana tasks and generates training data for fine-tuning an OpenAI GPT model. It uses Asana and OpenAI APIs to fetch the task details, process them, and store the extracted data in JSON format.

## Features
- Extract test case data from Asana tasks using Asana API.

- Generate training data in JSONL format for OpenAI GPT model fine-tuning.

- Fine-tune an OpenAI GPT model using the generated training data.

- Test the fine-tuned model with a given Asana task.


## Installation
1. Clone the repository

2. Navigate to the project directory:
`cd Asana-Extractor-For-Fine-Tune`

3. Install required Python packages:
`pip install -r requirements.txt`

4. Create a `.env` file in the root directory of the project and add your OpenAI API key:
```
ASANA_API_KEY=your_asana_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage
1. Open `get-fine-tune-data.py` and update the `task_ids` list with your actual list of Asana task IDs. Make sure to replace the example task IDs with the ones from your Asana tasks
2. Run the script: `python get-fine-tune-data.py`
The script will extract test case data from the specified Asana tasks, save the extracted data in the `defects` folder, and generate training data in JSONL format.

3. Fine-tune your OpenAI GPT model using the generated training data.

4. Open `test-fine-tune-model.py` and update the `task_gid` and `model_name` variables with the Asana task ID you want to process and your fine-tuned model ID, respectively.

5. Run the script:
`python test-fine-tune-model.py`


## License
MIT License. See LICENSE for more information.
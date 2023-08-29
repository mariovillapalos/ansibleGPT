import openai
import yaml


# Load the API Key from the YAML file
with open('./Openai/openai_config.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Session Key for the Chat GPT API
openai.api_key = data['openai']['api_key']

# Ask Chat GPT prompts with a reduce length.


def ask_gpt(prompt):
   
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.1,
    )
    
    message = response['choices'][0]['message']['content']
    
    return message
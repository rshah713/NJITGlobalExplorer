import os

from dotenv import load_dotenv
from together import Together

load_dotenv()

client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

def make_request(dataset, dataset_info, user_prompt):
    system_prompt = '''Your name is NJITGlobalExplorer, you are an AI model used in a data-visualization interactive dashboard displaying Study Abroad data with both National & NJIT specific datasets.
You are going to be given the data in JSON format and are to respond with the answer to the user's question using the data provided. Be specific when answering the user_query and cite data points if needed.
'''
    formatted_user = f'''data: {dataset}
dataset_description: {dataset_info}
user_query: {user_prompt}
'''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": formatted_user}
    ]
    response = client.chat.completions.create(
    model="meta-llama/Llama-3-8b-chat-hf",
    messages=messages,
    )
    return response.choices[0].message.content
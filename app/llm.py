import os

from dotenv import load_dotenv
from together import Together

load_dotenv()

client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

def make_request(dataset, dataset_info, user_prompt,system_prompt=None):
    if system_prompt is None:
        system_prompt = '''Your name is NJITGlobalExplorer, you are an AI model used in a data-visualization interactive dashboard displaying Study Abroad data with both National & NJIT specific datasets.
    You are going to be given the data in JSON format and are to respond with the answer to the user's question using the data provided. Be specific when answering the user_query and cite data points if needed (explicit citation at the bottom is not needed).

    The response should be short & direct and should not recite the datapoints back to the user.
    Example:
        user_query: What year has an abormally low % of Semester Abroad students?
        response: Based on the data, I can see that the year 2020 has an abnormally low percentage of semester abroad students for both national and NJIT-specific datasets. For the 'National - Semester' dataset, the percentage is 62.7, which is significantly higher than the other years. For the 'NJIT - Semester' dataset, the percentage is 5.9, which is significantly lower than the other years.
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

def generate_dataset_paragraph(dataset, dataset_info):
    system_prompt = '''You are a data-analysis agent tasked with generating paragraph long descriptions analyzing trends. Do not use first-person pronouns. Pick only 1-2 trends, response must be no more than 1 paragraph total. 
    Do not give conclusion/summaries (e.g. Overall, the data suggests...) or introductions (e.g. the dataset provided offers valuable insights into...)'''
    return make_request(dataset, dataset_info, 'Find some trends in this data', system_prompt=system_prompt)

import os
import json

from dotenv import load_dotenv
from together import Together

load_dotenv()

client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

def make_request(system_prompt, user_msg, convo_history=None):
    if system_prompt is None:
        system_prompt = '''Your name is NJITGlobalExplorer, you are an AI model used in a data-visualization interactive dashboard displaying Study Abroad data with both National & NJIT specific datasets. \
            You are going to be given the data in JSON format and are to respond with the answer to the user's question using the data provided. Be specific when answering the user_query and cite data points if needed (explicit citation at the bottom is not needed). \
    The response should be short & direct and should not recite the datapoints back to the user.
    Example:
        user_query: What year has an abormally low % of Semester Abroad students?
        response: Based on the data, I can see that the year 2020 has an abnormally low percentage of semester abroad students for both national and NJIT-specific datasets. For the 'National - Semester' dataset, the percentage is 62.7, which is significantly higher than the other years. For the 'NJIT - Semester' dataset, the percentage is 5.9, which is significantly lower than the other years.
    '''
    
    if convo_history:
        messages = convo_history
    else:
        messages = [
            {"role": "system", "content": system_prompt}
        ]

    messages.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=messages,
    )
    messages.append({"role": "assistant", "content":response.choices[0].message.content})
    # print("=> LLM Request with messages:")
    # for message in messages:
    #     print(f"  => {message}")
    return response.choices[0].message.content, messages

def get_dataset_info(chartName):
    if chartName == 'abroadParticipation':
        desc = 'The labels represent the states, the National dataset is the % of study abroad by state (e.g % of students that go abroad in NJ, VA, etc). \
            The NJIT line is consistent as it \
            represents % of NJIT students that study abroad in general at the university. When analyzing the NJIT line, ignore any state related info, \
                only use State related info for National dataset.'
    elif chartName == 'culturalCompetence' or chartName == 'professional':
        desc = "The labels represent questions asked to study abroad participants. Each dataset contains the % of people who resonate with the statement."
    else:
        desc = None
    
    return desc


def generate_dataset_paragraph(dataset, dataset_info=None):
    if list(dataset.keys())[0] != 'abroadParticipation':
        system_prompt = '''You are a data-analysis agent tasked with generating 6-8 sentence descriptions of a dataset. Do not use first-person pronouns. \
            Give a good summary of the data as a whole and include a brief comparative analysis between NJIT and National Study Abroad Programs. \
                It should be 6-8 sentences and it should be very specific. If the datapoints are less than the labels, assume, the rest of the points are null.\
                    Do not give conclusion/summaries (e.g. Overall, the data suggests...) or introductions (e.g. the dataset provided offers valuable insights into...).\
                        The last sentence should be a big-picture application of a trend or conclusion found from the data (should be directly related to data, not generic 'study other areas')
                        
                        '''
    else:
        system_prompt = '''You are a data-analysis agent tasked with generating 6-8 sentence descriptions of a dataset. Do not use first-person pronouns. \
            Give a good summary of the data as a whole and include a brief analysis of NJIT and National Study Abroad Programs seperately. \
                It should be 6-8 sentences and it should be very specific. If the datapoints are less than the labels, assume, the rest of the points are null.\
                    Do not give conclusion/summaries (e.g. Overall, the data suggests...) or introductions (e.g. the dataset provided offers valuable insights into...).\
                        *The last sentence should be a big-picture application of a trend or conclusion found from the data (should be directly related to data, not generic 'study other areas')*
                        
                        '''
    if dataset_info is None:
        dataset_info = get_dataset_info(list(dataset.keys())[0])
    system_prompt_ext = f"""
    data:{dataset}
        dataset_description: {dataset_info}
        """
    system_prompt += system_prompt_ext
    return make_request(user_msg='Find some trends in this data', system_prompt=system_prompt)


def chat_with_user(user_msg, datasets, convo_history):
    system_prompt = """You are NJITGlobalExplorer, a chatbot in a Study Abroad Analytics system on the NJIT Study Abroad website. Analyze user messages and structure a response based on provided data.

Consider:
- Conversation history (if available)
- User Message: The latest message from the user
- Data: Relevant datapoints from each dataset
- Dataset Sources: Descriptions of each dataset and their external sources

Write a response based on the User Message, ensuring it is backed by datapoints from the relevant dataset. Use the 'description' in the Dataset Sources for context of each dataset. If you cannot answer the User Message based on the provided data, say so. Write a conversational, short 1-3 sentence response that will be directly given to the user.
The last sentence of the response should cite the data that is used in the format "(Source: {sourceName}, {sourceOrgName})" from the relevant Dataset Sources UNLESS ASKING FOR MORE INFORMATION FROM USER.

The response should be JSON in the form {"response": "{response_to_be_generated_and_sent_to_user}"}.

Do not include any additional text or explanations or notes outside the JSON format. Make sure to cite the exact source name provided in the Dataset Sources.

"""
    dataset_sources = {
        "abroadParticipation": {
            'description': 'The study abroad % participation rate, where the National dataset is broken down by state, and the NJIT datapoints represent the overall study abroad participation rate at NJIT (ex. 1.01 = 1.01% of students study abroad)',
            'sourceOrgName': 'NAFSA Association of International Educators',
            'sourceLink': 'https://www.nafsa.org/sites/default/files/media/document/State%20by%20State%2021_22%20study%20abroad%20statistics.pdf',
            'sourceName':'U.S. STUDY ABROAD PARTICIPATION BY STATE'
        },
        'culturalCompetence': {
            'description': 'The labels represent questions asked to study abroad participants to gauge cultural competence. Each dataset contains the % of people who resonate with the statement.',
            'sourceOrgName': 'AIFS Abroad',
            'sourceLink': 'https://assets.aifsabroad.com/images/v1659032819/PDF/outcomes2018/outcomes2018.pdf?_i=AA',
            'sourceName': 'AIFS Study Abroad Alumni Outcomes: A longitudinal study of personal, intercultural and career development'
        },
        'durationData': {
            'description': 'Data on duration of study abroad for U.S. students studying outside of the United States vs NJIT students for academic credit. Duration abroad includes information on short-term, mid-length, and long term periods abroad.',
            'sourceOrgName': 'Institute of International Education',
            'sourceLink': 'https://opendoorsdata.org/data/us-study-abroad/duration-of-study-abroad/',
            'sourceName': 'IIE Open Doors Report'
        },
        'professional': {
            'description': 'The labels represent questions asked to study abroad participants to gauge career readiness. Each dataset contains the % of people who resonate with the statement.',
            'sourceOrgName': 'IES Abroad',
            'sourceLink': 'https://www.iesabroad.org/about/alumni-survey-results',
            'sourceName': 'Recent Graduates Survey: The Impact of Studying Abroad on Recent College Graduates Careers'
        }
    }
    
    
    system_prompt_ext = f"""
    {{
        "Data": {datasets},
        "Dataset Sources": {dataset_sources}
    }}
    """
    system_prompt += system_prompt_ext
    resp, convo_history = make_request(user_msg=user_msg, system_prompt=system_prompt, convo_history=convo_history)
    json_object = json.loads(resp[resp.find('{'):resp.find('}') + 1])
    return json_object.get('response', ''), convo_history
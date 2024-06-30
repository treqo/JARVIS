from groq import Groq
import os
from dotenv import load_dotenv
from PIL import ImageGrab

dotenv_path = os.path.join(os.path.dirname(__file__), './.env')
load_dotenv(dotenv_path=dotenv_path)

api_keys = {
    "openai": os.getenv('OPENAI_API_SECRET_KEY'),
    "groq": os.getenv('GROQ_API_SECRET_KEY')
}

groq_client = Groq(api_key=api_keys['groq'])

def groq_prompt(prompt):
    convo = [{'role': 'user', 'content': prompt}]
    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message

    return response.content

def function_call(prompt):
    sys_msg = ('''
You are an AI function calling model. You will determine whether extracting the users clipboard content, taking a screenshot, capturing the webcam or calling no functions is best for a voice assistant to respond to the users prompt. The webcam can be assumed to be a normal laptop webcam facing near the user. You will respond with only one selection from this list: ["extract clipboard", "take screenshot", "capture webcam", "None"]. Do not respond with anything but the most logical selection from that list with no explanations. Format the function call name exactly as I listed.
               ''')
    
    function_convo = [
        {'role': 'system', 'content': sys_msg},
        {'role': 'user', 'content': prompt}
    ]

    chat_completion = groq_client.chat.completions.create(messages=function_convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message

    return response.content

def take_screenshot():
    path = os.path.join(os.path.dirname(__file__), './assets/img/screenshot.jpg')
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15) # faster with low quality


def webcam_capture():
    return None

def get_clipboard_text():
    return None

prompt = input('USER: ')
function_response = function_call(prompt)
print(f'Function call: {function_response}')
response = groq_prompt(prompt)
print(response)

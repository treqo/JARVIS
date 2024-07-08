from groq import Groq
import os

class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_SECRET_KEY'))
        self.convo = [{'role': 'system', 'content': 'You are an AI voice assistant named Jarvis. Generate the most useful and factual response possible, carefully considering all previous generated text in your response before adding new tokens to the response. Make your response clear and concise, avoiding any verbosity.'}]

    def prompt(self, text):
        self.convo.append({'role': 'user', 'content': text})
        chat_completion = self.client.chat.completions.create(messages=self.convo, model='llama3-70b-8192')
        response = chat_completion.choices[0].message
        self.convo.append(response)
        return response.content
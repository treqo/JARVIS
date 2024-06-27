from openai import OpenAI

def get_client(api_key):
    return OpenAI(api_key=api_key)

def get_ai_response(client, messages):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            response += content
    print()  # New line after complete response
    return response

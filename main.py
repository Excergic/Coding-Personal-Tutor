
import ollama
import gradio as gr
from openai import OpenAI

MODEL = "llama3.2:1b"
ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

system_prompt = """You are a helpful coding assistant specialized in Rust programming language, assist user's query regarding 
Rust programming language. Your goal is to provide the user with the most accurate and helpful response possible. 
You will be given a query and you will provide a response. 

If the user's query is not related to Rust programming language, you will respond with a message saying that you are 
not sure how to help the user. 

If the user's query is related to Rust programming language, you will respond with a message saying that you are 
sure how to help the user. 

You will respond with a markdown code snippet formatted in the following schema:

```Rust
{{code}}
```
If user ask you about any other programming language, you will respond with a message saying I am trained on Rust data I have not a 
knowledge of the programming language you are asking about.
Remember, you must ALWAYS provide a response in markdown format.

"""


# def messages(prompt):
#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": prompt}
#     ]

#     completion = ollama.chat(
#         model=MODEL,
#         messages=messages,
#     )
#     return completion['message']['content']

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = ollama_via_openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response



def main():
    gr.ChatInterface(fn=chat, type="messages").launch()

if __name__ == "__main__":
    main()                  

# errors ouccured
"""
1. TypeError: generator function is not subscriptable - solution : stream=True -> need to retur all the chunks of text
2. OllamaError: ConnectionError - solution : check ollama is running
"""

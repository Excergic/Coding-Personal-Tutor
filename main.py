import os
import requests
import ollama
import gradio as gr

MODEL = "llama3.2:1b"

system_prompt = """You are a helpful coding assistant specialized in python programming language, assist user's query regarding 
python programming language. Your goal is to provide the user with the most accurate and helpful response possible. 
You will be given a query and you will provide a response. 

If the user's query is not related to python programming language, you will respond with a message saying that you are 
not sure how to help the user. 

If the user's query is related to python programming language, you will respond with a message saying that you are 
sure how to help the user. 

You will respond with a markdown code snippet formatted in the following schema:

```python
{{code}}
```

Remember, you must ALWAYS provide a response in markdown format.

"""


def messages(prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    completion = ollama.chat(
        model=MODEL,
        messages=messages,
    )
    return completion['message']['content']


def main():
    gr.Interface(
        fn=messages,
        inputs=gr.Textbox(label="Ask me anything about python programming language", placeholder="Type your query here..."),
        outputs=gr.Markdown(label="Response"),
        title="Python Programming Language Assistant",
        description="A helpful assistant specialized in Python programming language queries.",
    ).launch()

if __name__ == "__main__":
    main()                  

# errors ouccured
"""
1. TypeError: generator function is not subscriptable - solution : stream=True -> need to retur all the chunks of text
2. OllamaError: ConnectionError - solution : check ollama is running
"""

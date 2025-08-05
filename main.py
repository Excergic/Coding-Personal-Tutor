import os
import requests
import ollama

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


def user_prompt():
    query = input("Ask me anything about python programming language: ")
    return query

def messages():
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt()},
    ]

def get_response():
    response = ollama.chat(
        model=MODEL,
        messages=messages(),
        #stream=True,  
    )
    
    # collect all chunks of text from the response
    # full_respose = ""
    # for chunk in response:
    #     if 'message' in chunk and 'content' in chunk['message']:
    #         full_respose += chunk['message']['content']
    
    # return full_respose
    return response['message']['content']

def main():
    response = get_response()
    print(response)

if __name__ == "__main__":
    main()                  

# errors ouccured
"""
1. TypeError: generator function is not subscriptable - solution : stream=True -> need to retur all the chunks of text
2. OllamaError: ConnectionError - solution : check ollama is running
"""
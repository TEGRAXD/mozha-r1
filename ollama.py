from ollama import chat
from ollama import ChatResponse

# response: ChatResponse = chat(model="", messages=[
#     {
#         "role": "system",
#         "content": ""
#     }
# ])

# print(response)
# print(response.message.content)

stream = chat(model="mozha-q4_k_m:latest", messages=[
    {
        "role": "user",
        "content": "Hello, what is your name?"
    }
], stream=True)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
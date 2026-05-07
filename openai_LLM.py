import openai
from openai import OpenAI
import json

def calculator(a,b,operation):
    """
    Performs basic operations like addition and multiplications.

    Args:
    a: The First Number.
    b: The Second Number.
    operation: The operation to perform (eg. 'add' or 'multiply').
    """
    if operation == 'add':
        return a+b
    elif operation == 'multiply':
        return a*b
    return "Invalid Operation"

tools=[
    {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"Calc that performs basic operations",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number"},
                    "b":{"type":"number"},
                    "operation":{"type":"string"}
                }
            },
            "required":['a','b',"operation"]
        }
    }
]

user_input="What is 5 multiplied by 6?"

client= OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')

response=client.chat.completions.create(
    model='llama3',
    messages=[{"role":"user","content":user_input}],
    tools=tools
)

message=response.choices[0].message

if message.tool_calls:
    tool_call=message.tool_calls[0]
    args=json.load(tool_call.function.arguments)

    result=calculator(args['a'],args['b'],args['operation'])

    print(f"Total Result: {result}")

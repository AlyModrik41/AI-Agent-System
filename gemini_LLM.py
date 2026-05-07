import openai
import google.generativeai as genai
import json
import re
import wikipedia
import requests
from google.api_core import exceptions
import faiss
from sentence_transformers import SentenceTransformer
from LLMcash.LLMcache import LLMCache
import time
from langchain__ import langchain_agent

genai.configure(api_key="AIzaSyDOQdwu_NovzBjYTIVifIiZkZIxxsB9UkE")

user_input="Convert 300 USD TO EGP"

cache=LLMCache(ttl=600)

embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
dimension=384
index=faiss.IndexFlatL2(dimension)

memory_texts=[]

def run(query, mode="custom"):
    if mode == "custom":
        return run_agent(query)
    elif mode == "langchain":
        return langchain_agent.run_langchain(query)
    else:
        return "Invalid mode"

def store_memory(text):

    if text in memory_texts:
        return
    
    embedding=embedding_model.encode([text])
    index.add(embedding)
    memory_texts.append(text)

def retrieve_memory(query, k=2):

    if len(memory_texts) == 0:
        return []
    
    k=min(k,len(memory_texts))

    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:
        if idx < len(memory_texts):
            results.append(memory_texts[idx])

    return results


store_memory("Egypt population is 119 million")


def extract_action(output):

    match=re.search(r"Action:\s*(.*)",output)

    if not match:
        return None
    
    return match.group(1).strip()

def parse_args(action_line):
    args_str=re.search(r"\((.*)\)",action_line).group(1)

    raw_args=args_str.split(",")

    clean_args=[]

    for arg in raw_args:

        val=arg.split("=")[-1].strip().replace("'","").replace('"',"")
        clean_args.append(val)

    return clean_args

def calculator(a,b,operation):
    """
    Performs basic math operations like addition and multiplication.

    Args:
        a: The first number.
        b: The second number.
        operation: The operation to perform ('add' or 'multiply').
    """
    if operation == 'add':
        return a+b
    elif operation == 'multiply':
        return a*b
    return "Invalid_Operation"

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query,sentences=2)
        return result
    except:
        return "No Results Found !!"
    
def currency_exchange(from_currency,to_currency):

    url=f"https://open.er-api.com/v6/latest/{from_currency}"

    response=requests.get(url)
    response.raise_for_status()
    data=response.json()

    rate=data.get('rates',{}).get(to_currency)

    if rate:
        return rate
    
    return "Currency Not Found !!"

tools={
    "calculator":calculator,
    "search_wikipedia":search_wikipedia,
    "currency_exchange":currency_exchange
}

# models=[]


# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         models.append(m.name)

models = [             
    "gemini-2.0-flash",                    
    "gemini-2.5-flash",                    
    "gemini-2.5-pro-preview-tts",          
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemma-4-26b"
]


SYSTEM_PROMPT="""
You are an AI agent that can use tools.

STRICT RULES:
- Do Not generate Observation yourself
- Do Not generate Final Answer yourself
- Do Not use the same tool for the same thing more than one time in a row
- Try Getting the best sentence, so when you give it to wikipedia it will get the best results out.
- If sufficient information is available, proceed to Final Answer immediately
- For currency conversion ALWAYS use currency_exchange first.
  Do NOT use Wikipedia for exchange rates.

Format :

Thought: your reasoning
Action: tool_name(arguments)

Wait for Observation before continuing

Repeat until you reach the final answer.

Available Tools:
- calculator(a, b, operation)
- search_wikipedia(query)
- currency_exchange(from_currency,to_currency)

IMPORTANT:
- use search_wikipedia for factual questions
- use calculator for math
1. Get exchange rate
2. Use calculator to multiply amount by rate

When done:
Final Answer: your answer
"""

def generate_with_fallback(prompt):
    for model_name in models:
        try:
            print(f"Attempting with {model_name} ...")
            model=genai.GenerativeModel(model_name)
            response=model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            print(f"Quota reached for {model_name}. Switching...")
            continue
        except Exception as e:
            print(f"An unexpected error occurred with {model_name} : {e}")
            break
    return "All Models have exhausted their quota or failed"


def run_agent(query):

    cached=cache.get(("final",query))
    if cached:
        print("LLMCache Hit !!")
        return cached

    history=SYSTEM_PROMPT + "\nUser: "+ query+ "\n"
    relevant_memories = retrieve_memory(query)
    if relevant_memories:
        history += "\nRelevant Memories:\n"

        for mem in relevant_memories:
            history += f"- {mem}\n"
    result=None

    for _ in range(5):
        output=generate_with_fallback(history)

        print(f"\nModel:\n {output}")

        if "Final Answer:" in output:
            cache.set(("final",query),output)
            return output
        
        action_line=extract_action(output)

        tool_name=action_line.split("(")[0]

        if not action_line:
            continue
  
        if tool_name not in tools:
            result="Invalid Tool"
        else:
            args=parse_args(action_line)

            if tool_name == "calculator":
                a=float(args[0])
                b=float(args[1])
                op=args[2]

                if op in ["multiplication","multiply","*"]:
                    op = "multiply"
                elif op in ["addition", "add","+"]:
                    op= "add"
            
                result = tools[tool_name](a,b,op)
            
            elif tool_name == "search_wikipedia":
                result= tools[tool_name](args[0])
                store_memory(result)
            
            elif tool_name == "currency_exchange":
                result= tools[tool_name](args[0],args[1])
                store_memory(f"1 {args[0]} = {result} {args[1]}")
        
        history+=output+f"\nObservation: {result}"


    return "Max Steps Reached"

start=time.time()
run(user_input,mode="custom")
print(f"Latency: {time.time()-start:.2f}s")
run(user_input,mode="langchain")
print(f"Latency: {time.time()-start:.2f}s")



# chat=model.start_chat()

# response=chat.send_message(user_input)

# if response.candidates[0].content.parts[0].function_call:
#     call=response.candidates[0].content.parts[0].function_call

#     args=dict(call.args)
#     result=calculator(args["a"],args["b"],args["operation"])

#     print(f"Tool Result: {result}")
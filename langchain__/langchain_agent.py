from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import wikipedia
import requests

def wiki_tool(query):
    return wikipedia.summary(query,sentences=2)

def calculator_tool(a,b,op):

    if op == 'add':
        return a+b
    elif op == 'multiply':
        return a*b
    
    return "Invalid_Operation"


def currency_tool(query):
    from_currency, to_currency = query.split(",")
    url=f"https://open.er-api.com/v6/latest/{from_currency}"
    data=requests.get(url).json()
    return data["rates"].get(to_currency,"Not Found")

tools=[
    Tool(
        name="Wikipedia",
        func=wiki_tool,
        description="Searches Wikipedia"
    ),
    Tool(
        name="Currency",
        func=currency_tool,
        description="Converts currency like USD -> EGP"
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Used for mathematical operations"
    )
]

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key="YOUR_API_KEY"
)

langchain_agent=initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_langchain(query):
    return langchain_agent.run(query)

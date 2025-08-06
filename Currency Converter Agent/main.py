from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
import os
import requests
from langchain import hub
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
import json
load_dotenv()

HF_TOKEN=os.getenv('HF_TOKEN')
EXCHANGE_RATE_API_KEY=os.getenv('EXCHANGE_RATE_API_KEY')
prompt = hub.pull("hwchase17/react")

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=HF_TOKEN, 
    base_url="https://router.huggingface.co/v1",
)
@tool
def getCurrentCurrencyRate(Currencies) -> str:
    """Use this tool to check the exchange rate between two currencies, this function parameter accepts a dictionary with keys InputCurrency and RequiredCurrency"""
    Currencies=json.loads(Currencies)
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{Currencies['InputCurrency']}"
    response = requests.get(url=url).json()
    rate ={response["conversion_rates"][Currencies['RequiredCurrency']]}
    return f"ConvertedCurrency ={rate}{Currencies['RequiredCurrency']} "


tools = [getCurrentCurrencyRate]

agent = create_react_agent(llm=llm,tools=tools,prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  
)
reponse=agent_executor.invoke({'input':"Convert One dollar to PKR"})
print(reponse['output'])

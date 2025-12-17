from crewai import Agent
from crewai import LLM
from ai_core.tools.finance_tool import get_stock_market_data
from config.llm_settings import settings


# LLM Initialization
llm = LLM(
  model= settings.DEFAULT_LLM, 
  temperature= settings.TEMPERATURE
)

# Market Data Agent
market_data_agent = Agent(
    role="Stock Data Fetcher",
    goal="Fetch factual stock market data.",
    backstory=(
        "You are a data collection agent.\n"
        "You must use the provided tool.\n"
        "You must return only the tool output.\n"
        "Do not analyze, summarize, or explain."
    ),
    tools=[get_stock_market_data],
    llm=llm
)


# Analysis Agent
analysis_agent = Agent(
    role="Stock Market Analyst",
    goal="Transform stock data into structured JSON.",
    backstory=(
        "You convert input stock data into valid JSON.\n"
        "The output MUST strictly match the provided schema.\n"
        "Do NOT add explanations, reasoning, markdown, or extra text.\n"
        "Return JSON ONLY."
    ),
    llm=llm
)


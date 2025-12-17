from crewai import Task
from pydantic import BaseModel
from ai_core.agents import market_data_agent,analysis_agent


# Stock output schema
class StockOutput(BaseModel):
  stock_price: float
  market_cap: float
  week_52_high: float | str
  week_52_low: float | str
  analyst_rating: float | str
  recent_news: list[dict] | None
  trade_decision: str
  explanation: str
  research_summary: str  

# Fetching Task
fetching_task = Task(
    description="Fetch the current stock price for {company}.",
    agent=market_data_agent,
    expected_output="Raw stock data as JSON"
)

# Analysis Task
analysing_task = Task(
    description="""
    Analyze the stock data and return a structured JSON response.

    Decision rules:
    - BUY if price is near 52-week low
    - SELL if price is near 52-week high
    - HOLD otherwise

    Explanation:
    - 2–3 sentences explaining why the decision was made

    Research summary:
    - Two short paragraphs
    - Paragraph 1: performance, trend, price position
    - Paragraph 2: risks, opportunities, outlook

    Recent news:
    - 2–3 items
    - Each item must include title and summary

    Rules:
    - Output valid JSON only
    - No markdown, bullets, or extra text
    """,
    agent=analysis_agent,
    expected_output="Structured stock analysis JSON",
    output_pydantic=StockOutput
)







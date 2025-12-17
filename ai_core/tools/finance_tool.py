import yfinance as yf
from crewai.tools import tool
import json


# Finance Tool
@tool('stock_market_research_tool')
def get_stock_market_data(ticker: str):
  """Fetch stock price using yfinance."""
  try:
    stock = yf.Ticker(ticker)
    info = stock.info or {}

    history = stock.history(period='1d')
    if history.empty:
      raise ValueError('No price data available')
    stock_price = float(history['Close'].iloc[-1])

    data = {
      "stock_price": stock_price,
      "market_cap": info.get("marketCap"),
      "week_52_high":info.get("fiftyTwoWeekHigh"),
      "week_52_low":info.get("fiftyTwoWeekLow"),
      "analyst_rating":info.get('recommendationMean'),
      "news_list": [],
      "trade_decision":info.get("recommendationKey"),
    }

    for item in stock.news[:1]:
      content = item.get('content',{})
      data["news_list"].append({
        "title": content.get("title"),
        "summary": content.get("summary"),
      })
    
    
    return data
  
  except Exception as e:
    return {
      "error": True,
      "message": str(e),
      "ticker":ticker
    }
  

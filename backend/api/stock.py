import json
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from ai_core.crew import run_stock_pipeline


router = APIRouter(prefix="/stocks", tags=["Stocks"])


class StockRequest(BaseModel):
  company: str

class StockAnalysis(BaseModel):
  stock_price: float
  market_cap: float
  week_52_high: float | str
  week_52_low: float | str
  analyst_rating: float | str
  recent_news: list[dict]
  trade_decision: str
  explanation: str
  research_summary: str



@router.post('/analyze',response_model=StockAnalysis)
async def analyze_stock(request: StockRequest):
  try:
    result = run_stock_pipeline(request.company)
    return result.pydantic # type: ignore
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to fetch stock data: {e}")
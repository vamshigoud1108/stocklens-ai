from fastapi import FastAPI
from backend.api.stock import router as stock_router


app = FastAPI(
    title = 'Stock Analyzer API',
    description="API for stock analysis, including trade decisions, research summary, and recent news."
)


app.include_router(stock_router)

@app.get("/")
async def home():
    return {"message": "Welcome to Stock API"}
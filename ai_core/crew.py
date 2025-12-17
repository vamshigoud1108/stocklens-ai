from crewai import Crew
from ai_core.agents import market_data_agent,analysis_agent
from ai_core.tasks import fetching_task,analysing_task

def run_stock_pipeline(company: str):
  """ Runs the stock analysis pipeline using CrewAI. """
  try:
    crew = Crew(
      agents=[market_data_agent, analysis_agent],
      tasks=[fetching_task,analysing_task],
      verbose=True
    )
    result = crew.kickoff(inputs = {'company':company})
    return result
  
  except Exception as e:
    raise RuntimeError(f"Stock pipeline failed: {e}")
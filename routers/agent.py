import time
from fastapi import APIRouter
from schemas.agent import AgentRequest, AgentResponse
from text_to_sql.agent import run_agent
from logger import get_logger

router = APIRouter(prefix="/agent", tags=["SQL Agent"])
logger = get_logger(__name__)

@router.post("/sql", response_model=AgentResponse)
def run_sql_agent(request: AgentRequest):
    """
    Mini SQL Agent (Task 4)
    Takes a natural language question, decomposes it, generates a SQL query,
    executes it in PostgreSQL with up to 3 error retries, and returns a natural
    language summary of the result.
    """
    logger.info(f"POST /agent/sql received question: {request.question}")
    
    start_time = time.time()
    
    # Run the core agent loop
    result = run_agent(request.question)
    
    elapsed = (time.time() - start_time) * 1000
    logger.info(f"Agent finished in {elapsed:.2f} ms with status: {result['status']}")
    
    return AgentResponse(**result)

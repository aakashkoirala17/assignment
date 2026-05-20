from pydantic import BaseModel, Field
from typing import Any, Optional

class AgentRequest(BaseModel):
    question: str = Field(..., description="The natural language question to process")

class AgentResponse(BaseModel):
    sql: str = Field(..., description="The final generated SQL query")
    result: Any = Field(..., description="The result rows or count returned from PostgreSQL")
    summary: str = Field(..., description="Natural language summary of the result")
    status: str = Field(..., description="Status of the agent execution (success or error)")
    error: Optional[str] = Field(None, description="Any error message if status is error")

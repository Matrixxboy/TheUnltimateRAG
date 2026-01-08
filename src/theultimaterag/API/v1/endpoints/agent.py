from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from langchain_core.messages import HumanMessage
from theultimaterag.core.container import rag_engine
from theultimaterag.core.workflows.engine import WorkflowEngine
from theultimaterag.utils.Response_Helper import make_response
from theultimaterag.utils.Response_Helper_Model import HTTPStatusCode, APICode

router = APIRouter()

# --- Schemas ---

class AgentSearchRequest(BaseModel):
    query: str = Field(..., description="The search query.")
    k: int = Field(5, description="Number of results to return.")
    user_id: Optional[str] = Field(None, description="User ID for RBAC. If None, only common data is searched.")
    filter: Optional[Dict[str, Any]] = Field(None, description="Metadata filter.")

class AgentSummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize.")
    instruction: Optional[str] = Field(None, description="Specific summarization instructions.")

# --- Endpoints ---

@router.post("/search")
async def agent_search(request: AgentSearchRequest):
    """
    Raw semantic search endpoint for agents.
    Returns a list of document chunks with their metadata.
    """
    try:
        # Construct filter similar to RAG logic
        filter_criteria = request.filter or {}
        
        # Enforce RBAC if user_id is provided, else public only
        if request.user_id:
            # If valid filter passed, we merge with RBAC. 
            # Note: Complex filter merging might be tricky with $or. 
            # For simplistic agent access, we might default to standard RBAC logic provided in vector_store or rag_engine.
            # But vector_manager.similarity_search expects a single dict.
            # Let's manually build the RBAC filter if not present.
            if "$or" not in filter_criteria:
                 filter_criteria["$or"] = [
                    {"user_id": request.user_id},
                    {"access_level": "common"}
                 ]
        else:
             filter_criteria["access_level"] = "common"

        docs = rag_engine.vector_manager.similarity_search(
            query=request.query,
            k=request.k,
            filter=filter_criteria
        )
        
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
            
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Search successful",
            data={"results": results}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Search failed",
            error=str(e)
        )

@router.post("/summarize")
async def agent_summarize(request: AgentSummarizeRequest):
    """
    Utility endpoint to summarize text using the system's LLM.
    """
    try:
        prompt_text = request.instruction or "Summarize the following text concisely:"
        prompt = f"{prompt_text}\n\n{request.text}"
        
        response = rag_engine.llm.invoke([HumanMessage(content=prompt)])
        summary = response.content
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Summarization successful",
            data={"summary": summary}
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Summarization failed",
            error=str(e)
        )

@router.get("/tools")
async def get_tools():
    """
    Returns OpenAI-compatible tool definitions for this API.
    Agents can use this to understand how to interact with this system.
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": "Search the RAG knowledge base for information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query."
                        },
                        "k": {
                            "type": "integer",
                            "description": "Number of results (default 5)."
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "summarize_text",
                "description": "Summarize a given text using an LLM.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to summarize."
                        },
                        "instruction": {
                            "type": "string",
                            "description": "Optional specific instructions."
                        }
                    },
                    "required": ["text"]
                }
            }
        }
    ]
    
    return make_response(
        status=HTTPStatusCode.OK,
        code=APICode.OK,
        message="Tool definitions retrieved",
        data={"tools": tools}
    )

class WorkflowRequest(BaseModel):
    query: str
    workflow_type: str = "self-correcting"

@router.post("/workflow")
async def run_workflow(request: WorkflowRequest):
    """
    Run an advanced agentic workflow (e.g. Self-Correcting RAG).
    Returns the final answer and the trace of steps.
    """
    try:
        engine = WorkflowEngine()
        result = engine.run(request.query)
        
        return make_response(
            status=HTTPStatusCode.OK,
            code=APICode.OK,
            message="Workflow executed",
            data={
                "answer": result["generation"],
                "trace": result["steps"],
                "final_query": result["question"]
            }
        )
    except Exception as e:
        return make_response(
            status=HTTPStatusCode.INTERNAL_SERVER_ERROR,
            code=APICode.INTERNAL_SERVER_ERROR,
            message="Workflow failed",
            error=str(e)
        )

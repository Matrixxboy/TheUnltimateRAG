from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from theultimaterag.LLM.connection import get_llm

# --- Data Models ---

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the query, 'yes' or 'no'")

# --- Chains ---

def get_retrieval_grader():
    """
    Creates a chain ensuring the retrieved document is relevant to the question.
    """
    llm = get_llm()
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
    
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )
    
    retrieval_grader = grade_prompt | structured_llm_grader
    return retrieval_grader

def get_query_rewriter():
    """
    Creates a chain to rewrite the question for better retrieval.
    """
    llm = get_llm()
    
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
    for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
    
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question."),
        ]
    )
    
    question_rewriter = re_write_prompt | llm
    return question_rewriter

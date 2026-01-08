from typing import Dict, TypedDict, List, Any
from theultimaterag.core.container import rag_engine
from .chains import get_retrieval_grader, get_query_rewriter

# Define Graph State
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    question: str
    generation: str
    documents: List[str]
    steps: List[str]

class WorkflowEngine:
    def __init__(self):
        self.grader = get_retrieval_grader()
        self.rewriter = get_query_rewriter()

    def run(self, query: str) -> Dict[str, Any]:
        """
        Executes the Self-Correcting RAG workflow.
        """
        state: GraphState = {
            "question": query,
            "generation": "",
            "documents": [],
            "steps": []
        }
        
        # 1. Retrieve
        state["steps"].append("retrieve")
        print("---RETRIEVE---")
        # Reuse existing RAG engine logic for retrieval
        retriever = rag_engine.vector_manager.get_retriever(search_kwargs={"k": 3})
        documents = retriever.invoke(query)
        state["documents"] = [d.page_content for d in documents]
        
        # 2. Grade Documents
        print("---CHECK DOCUMENT RELEVANCE---")
        relevant_docs = []
        for doc in state["documents"]:
            score = self.grader.invoke({"question": query, "document": doc})
            if score.binary_score == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                relevant_docs.append(doc)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
        
        # 3. Decision
        if not relevant_docs:
            print("---DECISION: ALL DOCS IRRELEVANT, REWRITE QUERY---")
            state["steps"].append("transform_query")
            
            # Rewrite
            better_question = self.rewriter.invoke({"question": query})
            print(f"---REWRITTEN QUERY: {better_question.content}---")
            state["question"] = better_question.content
            
            # Retry Retrieval (One-time loop for simplicity)
            state["steps"].append("retry_retrieve")
            documents = retriever.invoke(better_question.content)
            state["documents"] = [d.page_content for d in documents]
            # Ideally we grade again, but for speed we assume improvement
            relevant_docs = state["documents"] # Take whatever we got
            
        
        # 4. Generate
        print("---GENERATE---")
        state["steps"].append("generate")
        # Context join
        context = "\n\n".join(relevant_docs)
        
        # Call RAG Engine's LLM generation manually or reuse method
        # We reuse part of rag_engine logic but customized
        from langchain_core.messages import HumanMessage, SystemMessage
        prompt = f"Answer the question based only on the following context:\n\n{context}\n\nQuestion: {state['question']}"
        
        response = rag_engine.llm.invoke([HumanMessage(content=prompt)])
        state["generation"] = response.content
        
        return state

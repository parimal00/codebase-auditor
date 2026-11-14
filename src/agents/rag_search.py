from src.vector_store.code_indexer import CodebaseVectorStore
from src.config.llm import get_llm
from langchain_core.messages import HumanMessage
from src.schemas.state import AuditState
from src.schemas.rag_response import RAGResponseSchema

def rag_search_node(state: AuditState) -> AuditState:
    """Performs semantic RAG retrieval and generates an answer using retrieved code context."""
    user_query = state.get("user_query", "")
    
    vector_store = CodebaseVectorStore()
    matches = vector_store.search_codebase(query=user_query, top_k=3)
    
    total_chars = sum(len(m["text"]) for m in matches)
    print(f"Context size: {total_chars} chars (~{total_chars // 4} tokens)")
    
    context_blocks = []
    for m in matches:
        file_path = m["metadata"].get("file_path")
        symbol_type = m["metadata"].get("type")
        symbol_name = m["metadata"].get("symbol_name")
        text = m["text"]
        
        block = f"--- File: {file_path} ({symbol_type}: {symbol_name}) ---\n{text}"
        context_blocks.append(block)
    
    joined_context = "\n\n".join(context_blocks)
    
    prompt = f"""
    You are a technical codebase assistant. Answer the user's question using ONLY the provided code context.
    
    Context:
    {joined_context}

    Question: {user_query}
    """
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(RAGResponseSchema)
    result: RAGResponseSchema = structured_llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "rag_response": result.model_dump(),
        "retrieved_matches": matches
    }
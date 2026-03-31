from langgraph.graph import StateGraph, END
from state import GraphState
from nodes import retrieve, graded_documents, web_search, generate, check_hallucination

def decide_web_search(state:GraphState):
    return "web_search" if state['web_fallback'] else "generate"

def decide_final(state:GraphState):
    if state["hallucination"] and state.get("retry_count", 0)< 3:
        return "generate"
    return END

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", graded_documents)
workflow.add_node("web_search", web_search) 
workflow.add_node("generate", generate)
workflow.add_node("check_hallucination", check_hallucination)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges("grade_documents", decide_web_search)
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", "check_hallucination")
workflow.add_conditional_edges("check_hallucination", decide_final)

app = workflow.compile()
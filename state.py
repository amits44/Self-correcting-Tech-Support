from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    question: str
    generation: str
    web_fallback: bool
    hallucination: bool
    retry_count: int
    documents: List[str]
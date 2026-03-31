from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

llm = ChatOllama(model="qwen3:4b-instruct-2507-q4_K_M", temperature=0)

class GradeDocuments(BaseModel):
    binary_score: str = Field(description="'yes' or 'no'")

grader_llm = llm.with_structured_output(GradeDocuments)
relevance_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a relevance grader. Given a user question and a retrieved document, "
               "output 'yes' if the document is relevant, 'no' otherwise."),
    ("human", "Question: {question}\n\nDocument: {document}"),
])
relevance_grader = relevance_prompt| grader_llm

class GradeHallucination(BaseModel):
    binary_score: str = Field(description="'yes' if grounded, 'no' if hallucinating")

hallucination_grader = ChatPromptTemplate.from_messages([
    ("system", "Check if the generation is grounded in the provided documents. 'yes' = grounded."),
    ("human", "Documents: {documents}\n\nGeneration: {generation}"),
]) | llm.with_structured_output(GradeHallucination)

AnswerGrader = (
    ChatPromptTemplate.from_messages([
        ("system", "Does this answer address the question? 'yes' or 'no'."),
        ("human", "Question: {question}\n\nAnswer: {generation}"),
    ]) | llm.with_structured_output(GradeHallucination)
)
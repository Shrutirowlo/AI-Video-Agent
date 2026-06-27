from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough , RunnableLambda
import os

def get_llm():
    return ChatMistralAI(model = "mistral-small-latest",mistral_api_key = os.getenv("MISTRAL_API"),temperature = 0.3)

def build_chain(system_prompt : str):
    llm = get_llm()
    return(
        RunnablePassthrough() | RunnableLambda(lambda x :{"text":x}) |
        ChatPromptTemplate.from_messages([
            ("system",system_prompt ),
            ("human" , "{text}")
            
        ]) | llm | StrOutputParser()
    )

def extract_action_items(transcript : str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst .From the meeting transcripts."
        "Extract all action items.for each provide\n"
        "-Task description\n"
        "-Owner(who is responsibe)\n"
        "-Deadline(if mentioned else return 'Not specified'\n)"
        "Format as a numbered list.if none found say 'no action item found.' "
    )
    return chain.invoke(transcript)

def extract_key_decisions(transcript : str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst .From the meeting transcripts."
        "Extract all key decision made ,Format as a numbered list"
        "if none found say 'No key decision found.' "
    )
    return chain.invoke(transcript)

def extract_questions(transcript : str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst .From the meeting transcripts."
        "Extract all unresolved question"
        "Or topics needing follow-up.Format as a numbered list"
        "if none found say 'No question found.' "
    )
    return chain.invoke(transcript)


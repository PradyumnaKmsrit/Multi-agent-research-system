from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import duckduckgo_search, fetch_and_clean_page
from dotenv import load_dotenv
import os

load_dotenv()

# model setup
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


TOOL_DISCIPLINE_PROMPT = (
    "You must ONLY use the tools explicitly provided to you. "
    "Do not invent, reference, or call any tool that is not in your tool list. "
    "Always use the exact tool names given to you."
)

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[duckduckgo_search],
        system_prompt=TOOL_DISCIPLINE_PROMPT
    )

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[fetch_and_clean_page],
        system_prompt=TOOL_DISCIPLINE_PROMPT
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.
Topic: {topic}
Research Gathered:
{research}
Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)
Be detailed, factual and professional."""),
])
writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.
Report:
{report}
Respond in this exact format:
Score: X/10
Strengths:
- ...
- ...
Areas to Improve:
- ...
- ...
One line verdict:
..."""),
])
critic_chain = critic_prompt | llm | StrOutputParser()  
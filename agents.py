import os
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, web_scrape

load_dotenv()

# ==========================================
# LLM Configuration
# ==========================================

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "google/gemini-3.1-flash-lite"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("Model:", MODEL_NAME)
print("Base URL:", "https://openrouter.ai/api/v1")
print("Key Prefix:", OPENROUTER_API_KEY[:10])

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=2000,
)

# ==========================================
# Search Agent
# ==========================================

def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt="""
You are a research search agent.

Your task:

1. Search for recent and reliable information.
2. Always use the web_search tool before answering.
3. Identify useful subtopics.
4. Return relevant URLs.
5. Summarize important findings.

Focus on factual information.
"""
    )


# ==========================================
# Reader Agent
# ==========================================

def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[web_scrape],
        prompt="""
You are a web content analyst.

Your task:

1. Identify the most relevant URL.
2. Use the web_scrape tool.
3. Extract detailed content.
4. Summarize important findings.

Always provide:

URL Used:
Summary:
Important Findings:
"""
    )


# ==========================================
# Writer Chain
# ==========================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert researcher and technical writer.

Use only the supplied research.

Do not invent information.

Write detailed and factual reports.
"""
    ),

    (
        "human",
        """
Topic:
{topic}

Research Material:

{research}

Write a report with the following sections:

1. Introduction

2. Key Findings
- At least 3 detailed points

3. Conclusion

4. Sources
(List URLs used)

Make the report clear and well-structured.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ==========================================
# Fact Checker Chain
# ==========================================

fact_checker_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert fact checker.

Review the report carefully.

Identify:

- Unsupported claims
- Missing information
- Possible inaccuracies

Provide:

Fact Check Summary

Potential Issues

Confidence Score (/10)
"""
    ),

    (
        "human",
        """
Research Report:

{report}
"""
    )
])

fact_checker_chain = (
    fact_checker_prompt
    | llm
    | StrOutputParser()
)


# ==========================================
# Critic Chain
# ==========================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a sharp and constructive research critic.

Evaluate quality honestly.

Provide actionable feedback.
"""
    ),

    (
        "human",
        """
Research Report:

{report}

Fact Checker Notes:

{fact_check}

Respond EXACTLY in this format:

Score: X/10

Strengths:
- ...
- ...

Areas for Improvement:
- ...
- ...

One Line Verdict:
...
"""
    )
])

critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)
# pip install langchain langchain-community langchain-ollama duckduckgo-search

try:
    from langchain_ollama import ChatOllama
except Exception:
    from langchain_community.chat_models import ChatOllama

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun


# RENDER tools into text and freeze into the prompt
try:
    from langchain.tools.render import render_text_description   # newer
except Exception:
    from langchain_core.tools import render_text_description     # older


search_tool = DuckDuckGoSearchRun(name="searchWeb")
tools = [search_tool]
tool_desc = render_text_description(tools)

llm = ChatOllama(model="llama3.1:8b", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     
     "You are a careful assistant. You can use tools to answer questions.\n"
     "Add the source of the information"
     f"Available tools:\n{tool_desc}\n"   # << pre-filled text
     "Use tools for fresh info, then give a concise final answer."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# print(agentExecutor.invoke({"input": "What's the latest Python stable version?"}))

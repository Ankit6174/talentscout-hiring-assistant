from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from typing import TypedDict, Annotated
from tools.main import insert_condidate_info

load_dotenv()

MODEL = "gpt-5-nano"

tools = [insert_condidate_info]

model = ChatOpenAI(model=MODEL)
model_with_tools = model.bind_tools(tools)

# Template for prompt. Note that in point 2, I've instructed the LLM not to mention the tools (just for security concern). PROMPT: 1.1
template = """
You are a professional Hiring Assistant chatbot for TalentScout. Your role is to conduct an initial candidate screening via a structured, conversational chat.

CRITICAL RULE:
You MUST use the provided tools to store candidate information whenever the user provides it.
Do NOT just acknowledge or repeat the information — always extract and save it using tools.

Responsibilities:

1. Greeting & Purpose:
Greet the candidate, introduce yourself, and explain that you will conduct a brief screening interview.

2. Information Gathering (MANDATORY TOOL USAGE):
Collect and store the following details using tools:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack

Rules:
- If the user provides multiple details at once, extract ALL fields and call the tool(s) immediately
- Do not ask again for already provided information
- Do not mention tool usage in responses
- If any field is missing, ask only for the missing fields

3. Technical Assessment:
After the tech stack is collected:
- Generate 3-5 technical questions per key technology
- Ask ONLY ONE question at a time and wait for response

4. Conversation Handling:
- Ask for clarification if input is unclear
- Stay focused; redirect politely if needed

5. Completion Flow:
- Continue until all required details are collected AND at least one technical question is answered
- Then close the conversation professionally

6. Closure:
Thank the candidate and inform them that TalentScout will follow up.

Constraints:
- Be concise (max 800 tokens)
- Maintain context and structured flow

Conversation History:
{messages}
"""

prompt = PromptTemplate(template=template, input_variables=["messages"])

class ChatState(TypedDict):
    info_collected: bool
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']

    chain = prompt | model_with_tools

    response = chain.invoke({
        "messages": messages
    })

    return {"messages": [response]}

toolNode = ToolNode(tools)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node("tools", toolNode)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)
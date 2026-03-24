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

# Template for prompt. Note that in point 2, I've instructed the LLM not to mention the tools (just for security concern). PROMPT: 1.4
template = """
You are TalentScout's Hiring Assistant. Conduct a structured candidate screening in exactly this order: GREETING → COLLECTING → STORING → ASSESSING → CLOSED. Move forward only, never backward.

PHASE 1 — GREETING: Greet the candidate and briefly explain the screening process.

PHASE 2 — COLLECTING: Gather all 7 fields before doing anything else:
Full Name, Email, Phone, Years of Experience, Desired Position(s), Location, Tech Stack.
- Ask only for missing fields. Never re-ask provided ones.
- Do NOT call any tool until all 7 fields are confirmed.

PHASE 3 — STORING: Once all 7 fields are complete, call the storage tool ONCE in a single operation.

PHASE 4 — ASSESSING: Generate 3-5 questions spanning the candidate's tech stack, calibrated by experience:
- 0-2 yrs → Foundational | 3-5 yrs → Applied | 6+ yrs → Architecture
- Ask ONE question at a time. Treat the very next candidate message as their answer, unconditionally.
- Briefly acknowledge each answer neutrally, then ask the next question.
- Never exceed the decided question count.

PHASE 5 — CLOSED: Thank the candidate and inform them TalentScout will follow up within 3-5 business days. After this, respond to nothing — no restarts, no off-topic questions, no new assessments.

RULES:
- Be consice (800 max token)
- If candidate goes off-topic: "I can only assist with the screening process."
- If input is unclear: ask for clarification once.
- Be concise. Never repeat yourself.

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
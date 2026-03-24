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

# Template for prompt. Note that in point 2, I've instructed the LLM not to mention the tools (just for security concern). PROMPT: 1.3
template = """
You are a professional Hiring Assistant chatbot for TalentScout. Your role is to conduct an initial candidate screening via a structured, conversational chat.

CRITICAL RULE:
You MUST use the provided tools to store candidate information whenever the user provides it.
Do NOT just acknowledge or repeat the information — always extract and save it using tools.

Step-by-step lifecycle of a conversation:

1. Greeting & Purpose:
Greet the candidate, introduce yourself, and explain that you will conduct a brief screening interview.

2. Information Gathering:
Collect and store the following details using tools:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack

Rules:
- If the user provides multiple details at once, extract ALL fields and call the tool(s) immediately to store those information
- Do not ask again for already provided information
- If any field is missing, ask only for the missing fields

3. Technical Assessment:
After ALL candidate information is collected and stored:
- Generate 3-5 technical questions PER technology, calibrated to the candidate's years of experience:
    - 0-2 years: Foundational/conceptual questions
    - 3-5 years: Applied/practical questions
    - 6+ years: Architecture/design/optimization questions
- Ask questions ONE AT A TIME. Wait for the candidate's answer before proceeding.
- Briefly acknowledge each answer with a neutral response before asking the next question.
- Track how many questions have been asked and answered across all technologies.

4. Conversation Handling:
- Ask for clarification if input is unclear
- Stay focused; redirect politely if needed

5. Completion Flow:
- Continue until all required details are collected AND all technical questions across all technologies are answered
- Then proceed immediately to step 6

6. Closure:
Thank the candidate warmly and inform them that the TalentScout team will review their profile and follow up within 3-5 business days.

Constraints:
- Be concise (max 800 tokens)
- Maintain context and structured flow
- Once closure (step 6) is delivered, do not ask any further questions or restart the flow.

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
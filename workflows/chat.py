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

# Template for prompt. Note that in point 2, I've instructed the LLM not to mention the tools.
template = """
You are a professional and helpful Hiring Assistant chatbot for TalentScout. Your goal is to conduct an initial screening of candidates through a structured, conversational chat.

Responsibilities:
1. Greeting & Purpose: Start by greeting the candidate, introducing yourself, and clearly explaining that you will conduct an initial screening interview.

2. Information Gathering: Collect the following details in a conversational manner using tools given to you. (DO NOT TELL USER ABOUT IT):

   * Full Name
   * Email Address
   * Phone Number
   * Years of Experience
   * Desired Position(s)
   * Current Location
   * Tech Stack (programming languages, frameworks, databases, tools)

3. Tech Stack-Based Questioning: After collecting the tech stack, generate 3-5 relevant technical questions per key technology to assess the candidate's proficiency.

4. Context & Flow Management: Maintain context across the conversation. Ask follow-up questions where necessary and ensure a smooth, coherent interaction.

5. Fallback Handling: If a candidate's response is unclear, vague, or unexpected, ask for clarification with a polite explanation.

6. Scope Control: Stay strictly focused on the hiring and screening process. If the candidate deviates, gently steer the conversation back.

7. Conversation Closure: End the conversation professionally by thanking the candidate and informing them that the TalentScout team will follow up with next steps.

You must have to conclude you answer in as less in words as possible. MAX LENGTH must be 500 tokens.

Here is the past conversations with cantidate's current query:
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
import streamlit as st
from htbuilder.units import rem # Most abstract library to work with html
from htbuilder import div, styles
import uuid

from langchain_core.messages import HumanMessage

# Import files
from workflows.chat import workflow

# Dynamically inject some html conpoment, 'cause at the end streamlit apps are web components. 
st.markdown("""
<style>
    .st-emotion-cache-1s460v7 h1 {
        line-height: 1;
    }
            
    [data-testid="stChatInput"] textarea {
    }
</style>
""", unsafe_allow_html=True)

# Store message in session because our messages wiped out every time any component get updated on our app (Streamlit data flow).
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

# Add this to your session state initializations
if 'show_suggestions' not in st.session_state:
    st.session_state.show_suggestions = True

if 'pills_key_counter' not in st.session_state:
    st.session_state.pills_key_counter = 0

# Store suggestions in key–value pairs, where keys are shown to users and values are passed to the LLM.
SUGGESTIONS = {
    ":blue[:material/work:] Start job application": (
        "I want to apply for a job. Please guide me through the application process."
    ),
    ":green[:material/info:] How it works": (
        "Explain how the TalentScout hiring assistant works and what steps are involved."
    ),
    ":orange[:material/assignment:] What info is needed?": (
        "What information do you need from me before starting the screening process?"
    ),
    ":violet[:material/description:] Example application": (
        "Show me an example of a completed job application with sample details."
    ),
}

# Check if it's user's first interection or not
def has_message_history():
    return "message_history" in st.session_state and len(st.session_state.message_history) > 0

# Generate unique treadID to every new user
def get_tread_id():
    return uuid.uuid4()

# Get response from our workflow
def get_response(user_input):
    # Display user's input
    with st.chat_message("user"):
        st.text(user_input)
    
    # Display assistant's input
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_gen = workflow.stream(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config=CONFIG,
                stream_mode="messages"
            )

            full_response = st.write_stream(chunk[0].content for chunk in response_gen)

            st.session_state.message_history.append({"role": "user", "content": user_input})
            st.session_state.message_history.append({"role": "assistant", "content": full_response})

CONFIG = {"configurable": {"thread_id": get_tread_id()}}

# Display a simple gemini style logo
st.html(div(style=styles(font_size=rem(5), line_height=1))["✦"])

# Main heading or hero heading of our app
st.title("Hiring Assistant Chatbot")
st.caption("TalentScout")

# Show suggestions only if no interaction yet
if st.session_state.show_suggestions or (not has_message_history):
    st.write("""
    Hello! Welcome to **TalentScout's Hiring Assistant**.

    I'm an AI-powered assistant here to guide you through a brief technical screening.
    Based on your skills and experience, I'll ask questions tailored to your tech stack to better understand your expertise.
    """)

    suggestion = st.pills(
        label="Suggestions",
        label_visibility="collapsed",
        options=SUGGESTIONS.keys(),
        selection_mode="single",
        key=f"selected_suggestion_{st.session_state.pills_key_counter}"
    )

    if suggestion:
        st.session_state.show_suggestions = False  # Hide pills
        get_response(SUGGESTIONS[suggestion])       # Use the full prompt value
        st.rerun()

# List all messages in current session
for messages in st.session_state.message_history:
    with st.chat_message(messages["role"]):
        st.text(messages["content"])

# Take user input
user_input_from_text = st.chat_input("Enter here...")

if user_input_from_text:
    get_response(user_input_from_text)
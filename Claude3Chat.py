import streamlit as st
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

st.title("Claude 3 (Opus) Chat")

# Initialize chat history and prompt messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.prompt_messages = []

# API Key input field
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
api_key = st.text_input("API Key", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key

# Check if API key is provided before displaying chat
if api_key:
    model = "claude-3-opus-20240229"  # Change the model name as needed

    # Initialize the Anthropic model
    llm = Anthropic(api_key=api_key, model=model)

    with st.chat_message("assistant"):
        st.write("Hello 👋")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_input := st.chat_input("Say Something"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Append the new user message to prompt_messages
        st.session_state.prompt_messages.append(ChatMessage(role="user", content=user_input))

        # Get response from Anthropic model
        response = llm.chat(st.session_state.prompt_messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        response = str(response)

        # Add assistant response to chat history and prompt messages
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.prompt_messages.append(ChatMessage(role="assistant", content=response))

    # Refresh chat button
    if st.button("Refresh Chat"):
        # Clear chat history and prompt messages
        st.session_state.messages = []
        st.session_state.prompt_messages = []
        # Rerun the app to refresh the UI
        st.experimental_rerun()
else:
    st.write("Please enter your API key to start chatting.")

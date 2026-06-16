import os
import requests
import streamlit as st

st.set_page_config(page_title="Marketing AI", page_icon="🚀", layout="centered")

API_URL = os.getenv("API_URL", "http://15.206.164.222:8000/api/v1/chat")

# Sidebar for settings
st.sidebar.title("Settings")
user_id = st.sidebar.text_input("User ID", value="a14d2b6c-a849-4432-ba79-6e2fd1c38369")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Available test users:\n"
    "- `a14d2b6c-a849-4432-ba79-6e2fd1c38369`\n"
    "- `52ae2147-d7ec-497c-8358-c7eab3cd2c9c`"
)

# Main chat interface
st.title("Kiki 🚀")
st.markdown("Ask me anything about your marketing strategy, SEO, or check your support tickets!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your marketing question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    full_response = ""
    error_msg = ""

    # Display thinking spinner OUTSIDE the chat message container to prevent UI ghosting/duplication
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                API_URL,
                json={"user_id": user_id, "query": prompt},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            full_response = data.get("response", "")
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to the backend server. Is uvicorn running on port 8000?"
        except requests.exceptions.Timeout:
            error_msg = "The request timed out. The backend may be overloaded — please try again."
        except requests.exceptions.HTTPError:
            error_msg = "Oops! We encountered a little hiccup processing your request. Please try again!"
        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"

    # Display assistant response or error
    if error_msg:
        st.error(error_msg)
    elif full_response:
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

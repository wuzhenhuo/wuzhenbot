import importlib
import streamlit as st
import os
import openai
importlib.reload(openai)
if "openai_key" in st.session_state:
    openai.api_key = st.session_state["openai_key"]
    openai.api_base = st.session_state["OPENAI_API_BASE"].rstrip("/")
    openai.api_type = st.session_state["OPENAI_API_TYPE"]
    openai.api_version = "2024-05-13-preview"
#print(os.environ['OPENAI_API_KEY'])
#print(os.environ['OPENAI_API_BASE'])
#print(os.environ['OPENAI_API_TYPE'])
#print(os.environ['OPENAI_ENGINE'])
# Load environment variables from .env file
# Set up your OpenAI API credentials

# Define the chatbot function
def chat_with_model(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        engine=os.environ['OPENAI_ENGINE'],
        messages=messages,
        max_tokens=4000,
    )
    return response.choices[0].message.content

# Streamlit app code
def main():
    st.title("Alexzhenwu'sChatbot")

    # Initialize session state for messages if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

        # Set initial system message with a specific role (e.g., Assistant)
        initial_message = {
            "role": "system",
            "content": "You are Batman. Your job is to save Gotham City from the Joker. The user is Gotham City's police chief. Help him with the job."
        }
        st.session_state['messages'].append(initial_message)

    # Render chat history container first	
    chat_history_container = st.container()

    # Display existing conversation		
    with chat_history_container:
        for message in st.session_state["messages"]:
            if(message["role"]=="user"):
                st.markdown(f"**You**: {message['content']}")
            elif (message["role"]=="assistant"):
                st.markdown(f"_Assistant_: {message['content']}")	    		

    # Add user input at the bottom of the page		    
    st.write("Type your message below:")
    user_input = st.text_input("Enter", key=len(st.session_state["messages"]))

    if user_input:
        # Append user message to the conversation
        new_message = {"role": "user", "content": user_input}
        st.session_state['messages'].append(new_message)

        # Get chatbot's response and append it to the conversation
        bot_response = chat_with_model(st.session_state['messages'])

        assistant_response = {"role": "assistant", "content": bot_response}
        st.session_state["messages"].append(assistant_response)

        # We need to manually rerun the Streamlit script so that Streamlit can process the new state and display it
        st.experimental_rerun()


if __name__ == "__main__":
    main()

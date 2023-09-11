import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
import logging
from utils import initialize_session_state, display_ui_elements, generate_preparation_guide

# Setting up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Set the title of the Streamlit app
st.title("Technical Interview Preparation Guide")

# Model selection and token limit
models = ["gpt-3.5-turbo", "gpt-4"]
selected_model = st.selectbox("Select your preferred GPT model:", models)
token_limit = st.slider("Set the token limit for the output:", 50, 2048, 2048)

# Check for the OPENAI_API_KEY environment variable
API = os.environ.get("OPENAI_API_KEY")

# If the API key isn't found in environment variables, allow the user to input it
if not API:
    API = st.text_input("Enter your OpenAI API key:", type="password")
    if not API:
        st.warning("Please provide your OpenAI API key. Get it from [here](https://platform.openai.com/account/api-keys).\n")

# If an API key has been provided, create an OpenAI language model instance
if API:
    llm = ChatOpenAI(model=selected_model, temperature=0.7, openai_api_key=API, max_tokens=token_limit)

# Initialize session state
initialize_session_state()

# Fill with Sample Data button
if st.button("Fill with Sample Data"):
    st.session_state.name = "Ivan Ivanov"
    st.session_state.years_experience = "5"
    st.session_state.preferred_language = "Java"
    st.session_state.project_description = "Developed an Java application that is used by the Sales Engineers at Lufthansa Technic for creating offers for airplane engine repairs. It had an Handling Charges, Pricing Escalations for each year, Subcontract margins and etc."
    st.session_state.learning_style = "practical"
    st.session_state.focus_area = "design patterns"

# Display UI elements and get user input
user_input = display_ui_elements()

if API:
    llm = ChatOpenAI(model=selected_model, temperature=0.7, openai_api_key=API, max_tokens=token_limit)# Generate preparation guide
    generate_preparation_guide(user_input, llm)
    with st.sidebar:
        st.title("Responses", help="Displays the responses from the OpenAI API made during this session. **Refreshing or closing the tab will cause the list to be deleted!**")
        for idx, response in enumerate(st.session_state.chat_responses):
            # Truncate the chat message to a certain length (e.g., 50 characters)
            truncated_response = (response[:50] + '...') if len(response) > 50 else response
            
            with st.container():
                # Create an expandable section for each chat
                with st.expander(truncated_response, expanded=False):
                    st.write(response)

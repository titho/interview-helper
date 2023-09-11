import os
import uuid
import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import logging
from topics import topics
from info_preferences import info_preferences


def initialize_session_state():
    # Generate a unique session ID if it doesn't exist
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if 'prompts' not in st.session_state:
        st.session_state.prompts = []
        st.session_state.responses = []

    # Initialize session state values if they don't exist
    if 'name' not in st.session_state:
        st.session_state.name = ""
        st.session_state.years_experience = ""
        st.session_state.preferred_language = ""
        st.session_state.project_description = ""
    
    if 'chat_responses' not in st.session_state:
        st.session_state.chat_responses = []

def save_to_file(prompt, response):
    # Ensure the 'sessions' directory exists
    if not os.path.exists('sessions'):
        os.makedirs('sessions')
    
    filename = os.path.join('sessions', f"session_{st.session_state.session_id}.txt")
    with open(filename, 'a') as file:
        file.write(f"Prompt: {prompt}\n")
        file.write(f"Response: {response}\n")
        file.write("-----\n")

def display_ui_elements():
    name = st.text_input("Enter your name:", value=st.session_state.name, key="name_input")
    years_experience = st.text_input("Enter your years of technical experience:", value=st.session_state.years_experience, key="years_experience_input")
    preferred_language = st.text_input("Enter your preferred programming language:", value=st.session_state.preferred_language, key="preferred_language_input")
    project_description = st.text_area("Describe a project or domain you're familiar with:", value=st.session_state.project_description, key="project_description_input")

    # Integrating the display_info_preference function
    info_preference = display_info_preference()
    
    selected_topics = st.multiselect("Select the topics you're interested in:", list(topics.keys()), key="selected_topics_multiselect")

    selected_subtopics = {}
    for topic in selected_topics:
        selected_subtopics[topic] = st.multiselect(f"Select subtopics for {topic}:", topics[topic], key=f"subtopics_multiselect_{topic}")

    return {
        "name": name,
        "years_experience": years_experience,
        "preferred_language": preferred_language,
        "project_description": project_description,
        "info_preference": info_preference,
        "selected_topics": selected_topics,
        "selected_subtopics": selected_subtopics
    }

def display_info_preference():
    # Using a selectbox for info_preference input with a placeholder
    preference_options = [""] + list(info_preferences.keys())
    preference = st.selectbox("How would you like the information to be presented?", preference_options, key="info_preference_selectbox", index=0)

    # Displaying the tooltip for the selected preference using st.markdown and the title attribute
    if preference and preference != preference_options[0]:
        st.markdown(info_preferences[preference])
    
    return preference


def generate_preparation_guide(user_input, llm):
    if st.button("Generate Preparation Guide"):
        try:
            # Refining the prompt to be more instructional
            template = ("As a top-tier software engineering mentor, provide {name}, who has {years_experience} years of experience, a concise and direct tutorial on {selected_topics}, emphasizing {selected_subtopics}. Use {preferred_language} for coding examples and relate them to the {project_description} domain. Ensure the content aligns with the instruction: {info_preference}. Avoid introductory greetings or pleasantries.")

            # Create the PromptTemplate
            prompt_template = PromptTemplate(
                input_variables=["name", "years_experience", "preferred_language", "project_description", "info_preference", "selected_topics", "selected_subtopics"], 
                template=template
            )

            interview_prep_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="preparation_guide")

            # Use the user_input dictionary for the values
            results = interview_prep_chain(user_input)

            st.session_state.chat_responses.append(results['preparation_guide'])

            save_to_file(prompt_template, results['preparation_guide'])

            st.success(results['preparation_guide'])
        except Exception as e:
            # If there's an error, log it and show an error message
            logging.error("An error occurred:", exc_info=True)
            st.error("An error occurred. Please try again.")


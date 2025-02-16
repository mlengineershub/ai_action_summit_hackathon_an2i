import streamlit as st
import time
from openai import OpenAI
from workspace.src.utils import initialize_client
from workspace.src.propose_medical_queries import generate_search_propositions
from workspace.src.generate_follow_up_questions import generate_follow_up_questions
from workspace.src.generate_pertinent_points import extract_pertinent_medical_points
from workspace.src.gather_medical_knowledge_tool import generate_search_summary
from workspace.src.natural_google_search import summarize_google_research

# Initialize OpenAI client
client = initialize_client()

st.set_page_config(layout="wide")
st.title("Medical Assistant Dashboard")

# Sample conversation snippets for simulation
conversation_snippets = [
    ("Patient", "I've been experiencing severe headaches lately."),
    ("Doctor", "How long have you been having these headaches?"),
    ("Patient", "For about two weeks now. They're particularly bad in the morning."),
    ("Doctor", "Are they accompanied by any other symptoms?"),
    ("Patient", "Yes, sometimes I feel nauseous and sensitive to light."),
    ("Doctor", "Have you noticed any triggers for these headaches?"),
    ("Patient", "I think they get worse when I'm stressed or haven't slept well."),
    ("Doctor", "Are you taking any medications currently?"),
    ("Patient", "Just over-the-counter pain relievers, but they don't help much."),
]

# Initialize session state
if 'conversation_index' not in st.session_state:
    st.session_state.conversation_index = 0
    st.session_state.full_conversation = ""
    st.session_state.last_update_time = time.time()

# Create two columns: main content and search
col1, col2 = st.columns([2, 1])

with col1:
    # Conversation display
    st.subheader("Patient Consultation")
    conversation_container = st.container()
    
    # Medical queries, follow-up questions, and pertinent points
    queries_container = st.container()
    followup_container = st.container()
    points_container = st.container()

with col2:
    # Google Search section
    st.subheader("Medical Search")
    search_query = st.text_input("Enter medical search query")
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                search_results = summarize_google_research(client, search_query)
                st.write(search_results)

# Update conversation every 6 seconds
current_time = time.time()
if current_time - st.session_state.last_update_time >= 6 and st.session_state.conversation_index < len(conversation_snippets):
    role, message = conversation_snippets[st.session_state.conversation_index]
    st.session_state.full_conversation += f"{role}: {message}\n"
    st.session_state.conversation_index += 1
    st.session_state.last_update_time = current_time

# Display conversation
with conversation_container:
    st.text_area("Conversation", st.session_state.full_conversation, height=200)

# Generate and display medical queries, follow-up questions, and pertinent points
if st.session_state.full_conversation:
    # Medical Queries
    with queries_container:
        st.subheader("Suggested Medical Queries")
        queries_response = generate_search_propositions(client, st.session_state.full_conversation)
        if 'search_propositions' in queries_response:
            for query in queries_response['search_propositions']:
                if st.button(query):
                    with st.spinner("Gathering medical knowledge..."):
                        knowledge = generate_search_summary(client, query)
                        st.write(knowledge.get('summary', 'No summary available'))

    # Follow-up Questions
    with followup_container:
        st.subheader("Suggested Follow-up Questions")
        questions_response = generate_follow_up_questions(client, st.session_state.full_conversation)
        if 'follow_up_questions' in questions_response:
            for question in questions_response['follow_up_questions']:
                st.write("•", question)

    # Pertinent Points
    with points_container:
        st.subheader("Pertinent Medical Points")
        points_response = extract_pertinent_medical_points(client, st.session_state.full_conversation)
        if 'pertinent_points' in points_response:
            for point in points_response['pertinent_points']:
                st.write("•", point)

# Add auto-refresh to update the page every 6 seconds
st.empty()
time.sleep(6)
st.rerun()

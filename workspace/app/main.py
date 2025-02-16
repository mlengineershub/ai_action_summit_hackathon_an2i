import sys

# Add the app root to PYTHONPATH so that `workspace.src` is accessible
sys.path.insert(0, "/app")

import streamlit as st
import time
from workspace.src.utils import initialize_client
from workspace.src.propose_medical_queries import generate_search_propositions
from workspace.src.generate_follow_up_questions import generate_follow_up_questions
from workspace.src.tasks import generate_search_summary_task, search_articles_task

# Initialize OpenAI client
client = initialize_client()

st.set_page_config(layout="wide")
st.title("Virtual Doctor Consultation")

# Predefined conversation flow
CONVERSATION_FLOW = [
    {
        "role": "assistant",
        "content": "Hello, I'm Dr. AI. I'm here to help you today. What brings you in?",
    },
    {"role": "user", "content": "I have a headache and a sore throat."},
    {
        "role": "assistant",
        "content": "I understand. Have you experienced any fever recently?",
    },
    {"role": "user", "content": "Yes, I've had a fever for the past two days."},
    {
        "role": "assistant",
        "content": "I see. Have you taken any medication for these symptoms?",
    },
    {
        "role": "user",
        "content": "I've taken some paracetamol, but it hasn't helped much.",
    },
    {
        "role": "assistant",
        "content": "Based on your symptoms, I would recommend trying ibuprofen instead. It can help with both the fever and inflammation.",
    },
    {"role": "user", "content": "Okay, I'll try that. Thank you."},
    {
        "role": "assistant",
        "content": "Before you go, have you experienced any other symptoms I should know about?",
    },
    {"role": "user", "content": "No, just the headache and sore throat."},
    {
        "role": "assistant",
        "content": "Alright. Please take the ibuprofen as directed and rest well. If symptoms persist or worsen after 48 hours, please seek in-person medical attention. Take care!",
    },
]

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_index = 0
    st.session_state.last_update = time.time()
if "search_history" not in st.session_state:
    st.session_state.search_history = []  # Buffer for all searched queries and results
if "selected_search" not in st.session_state:
    st.session_state.selected_search = None
if "current_search_result" not in st.session_state:
    st.session_state.current_search_result = None
if "task_id" not in st.session_state:
    st.session_state.task_id = None

# Create two columns: one for the consultation and one for research/analysis
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Doctor Consultation")

    # Auto-advance the conversation every 10 seconds
    current_time = time.time()
    if (
        current_time - st.session_state.last_update >= 10
        and st.session_state.conversation_index < len(CONVERSATION_FLOW)
    ):
        st.session_state.messages.append(
            CONVERSATION_FLOW[st.session_state.conversation_index]
        )
        st.session_state.conversation_index += 1
        st.session_state.last_update = current_time
        st.rerun()

    # Display the chat messages
    for message in st.session_state.messages:
        role_display = "🩺 Doctor" if message["role"] == "assistant" else "👤 Patient"
        with st.chat_message(message["role"]):
            st.markdown(f"**{role_display}:** {message['content']}")

with col2:
    st.subheader("Quick Summarized Google Search")

    # --- Search Input & Proposition Display ---
    search_query = st.text_input(
        "Search medical topics:",
        key="google_search",
        placeholder="Enter medical topic to search...",
    )
    if search_query:
        with st.spinner("Searching medical literature..."):
            # Use Celery task for searching articles
            search_task = search_articles_task.delay(search_query)
            search_results = search_task.get()  # Wait for results

            # Use Celery task for generating summary
            summary_task = generate_search_summary_task.delay(
                search_query, search_results["results"]
            )
            summarized_search = summary_task.get()  # Wait for results

        st.markdown("**Select a search proposition:**")
        # Display the search results as markdown
        st.markdown(summarized_search.get("summary", "No summary available"))

    # --- Display Selected Search Result ---
    if st.session_state.selected_search:
        st.subheader("Search Results")
        st.write(f"You searched for: **{st.session_state.selected_search}**")
        st.info(st.session_state.current_search_result)

    # --- Additional Medical Analysis Sections ---
    if len(st.session_state.messages) > 1:
        # Combine messages into a single conversation text
        full_conversation = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages
        )

        # Relevant Medical Topics (now as clickable buttons)
        st.subheader("Relevant Medical Topics")
        queries_response = generate_search_propositions(client, full_conversation)
        if "search_propositions" in queries_response:
            for query in queries_response["search_propositions"]:
                if st.button(f"🔍 {query}", key=f"med_topic_{query}"):
                    st.session_state.selected_search = query

                    # Use Celery task for search and summary
                    search_task = search_articles_task.delay(query)
                    search_results = search_task.get()

                    summary_task = generate_search_summary_task.delay(
                        query, search_results["results"]
                    )
                    research_summary = summary_task.get()

                    st.session_state.current_search_result = research_summary.get(
                        "summary", "No summary available"
                    )
                    # Optionally add the search to the history buffer
                    st.session_state.search_history.append(
                        {
                            "query": query,
                            "summary": st.session_state.current_search_result,
                        }
                    )
                    st.rerun()  # Refresh to display the updated result

        # Proposed Follow-up Questions
        st.subheader("Proposed Follow-up Questions")
        questions_response = generate_follow_up_questions(client, full_conversation)
        if "follow_up_questions" in questions_response:
            for question in questions_response["follow_up_questions"]:
                st.write("🔍", question)

# --- Auto-Refresh ---
st.empty()
time.sleep(10)
st.rerun()

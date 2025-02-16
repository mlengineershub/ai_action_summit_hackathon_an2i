import sys

# Add the app root to PYTHONPATH so that `workspace.src` is accessible
sys.path.insert(0, "/app")

import streamlit as st
import time
from workspace.src.utils import initialize_client
from workspace.src.propose_medical_queries import generate_search_propositions
from workspace.src.generate_follow_up_questions import generate_follow_up_questions
from workspace.src.tasks import (
    generate_search_summary_task,
    search_articles_task,
    generate_report_task,
    detect_anomalies_task,
)

# Initialize OpenAI client
client = initialize_client()

st.set_page_config(layout="wide")
st.title("Virtual Doctor Consultation")

# Predefined conversation flow
CONVERSATION_FLOW = [
    {
        "role": "assistant",
        "content": "Hello, I'm Dr. Ahmed. I'm here to help you today. What brings you in?",
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

        # Display the search results as markdown
        st.markdown(summarized_search.get("search_summary", "No summary available"))

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

#         # Prescription Anomaly Detection
#         st.subheader("Prescription Anomaly Detection")

#         # Current Prescription Input
#         current_prescription = st.text_area(
#             "Current Prescription",
#             placeholder="Enter the current prescription...",
#             height=150
#         )

#         # Historical Prescription Input
#         historical_prescription = st.text_area(
#             "Patient's Medication History",
#             placeholder="Enter patient's medication history...",
#             height=150
#         )

#         # Example Data Button
#         if st.button("Load Example Data"):
#             st.session_state.current_prescription = """Patient: John Doe
# Date of Birth: 01/01/1970
# Date of Consultation: 01/01/2022
# Doctor: Dr. Jane Smith
# Medication: Amoxicillin 500mg
# Dosage: 1 capsule every 8 hours
# Duration: 7 days
# Refill: 0
# Instructions: Take with food"""
#             st.session_state.historical_prescription = """Patient: John Doe
# Date of Birth: 01/01/1970
# Previous Prescription (01/12/2021):
# Medication: Amoxicillin 500mg
# Prescribed: 1 capsule every 8 hours for 7 days
# Actual Usage: Patient took medication irregularly, missing several doses
# Notes: Patient reported difficulty maintaining schedule"""
#             st.rerun()

#         # Check for Anomalies Button
#         if st.button("Check for Prescription Anomalies"):
#             if not current_prescription or not historical_prescription:
#                 st.error("Please provide both current prescription and medication history.")
#             else:
#                 with st.spinner("Analyzing prescriptions for anomalies..."):
#                     # Use Celery task for anomaly detection
#                     anomaly_task = detect_anomalies_task.delay(
#                         current_prescription,
#                         historical_prescription
#                     )
#                     anomaly_results = anomaly_task.get()  # Wait for results

#                     # Display anomalies
#                     if "prescription_anomalies" in anomaly_results:
#                         st.markdown("### Detected Anomalies")
#                         for anomaly in anomaly_results["prescription_anomalies"]:
#                             st.warning(f"⚠️ {anomaly}")
#                     else:
#                         st.success("No prescription anomalies detected.")

# --- Report Generation ---
if st.session_state.conversation_index >= len(CONVERSATION_FLOW):
    st.subheader("Medical Report Generation")

    # Mock patient information
    patient_information = {
        "name": "John Smith",
        "age": "35",
        "gender": "Male",
        "ssn": "123-45-6789",
        "contact": "(555) 123-4567",
    }

    # Mock medical history
    medical_history = "No significant past medical history. No known allergies. No previous surgeries."

    # Mock prescription data
    current_prescription = """Patient: John Smith
Date of Birth: 01/01/1988
Date of Consultation: 02/16/2025
Doctor: Dr. Ahmed
Medication: Ibuprofen 400mg
Dosage: 1 tablet every 6 hours
Duration: 5 days
Refill: 0
Instructions: Take with food"""

    historical_prescription = """Patient: John Smith
Date of Birth: 01/01/1988
Previous Prescription (02/10/2025):
Medication: Paracetamol 500mg
Prescribed: 1 tablet every 6 hours for 3 days
Actual Usage: Patient reported taking 2 tablets every 4 hours
Notes: Patient reported inadequate pain relief"""

    if st.button("Generate Medical Report"):
        with st.spinner("Generating medical report and analyzing prescriptions..."):
            # Combine messages into conversation text
            full_conversation = "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages
            )

            # Generate report using Celery task
            report_task = generate_report_task.delay(
                full_conversation,
                patient_information,
                medical_history,
                "",  # Empty anomaly detection as we'll handle it separately
            )

            # Detect prescription anomalies using Celery task
            anomaly_task = detect_anomalies_task.delay(
                current_prescription, historical_prescription
            )

            # Get results from both tasks
            report_result = report_task.get()
            anomaly_results = anomaly_task.get()

            # Create two columns for report and anomalies
            report_col, anomaly_col = st.columns([2, 1])

            # Display the report in the left column
            with report_col:
                st.markdown("### Generated Medical Report")
                st.markdown("#### Symptoms")
                for symptom in report_result["symptoms"]:
                    st.markdown(f"- {symptom}")

                st.markdown("#### Pathology")
                st.markdown(report_result["pathology"])

                st.markdown("#### Treatment Plan")
                for treatment in report_result["treatment"]:
                    st.markdown(f"- {treatment}")

                st.markdown("#### Keywords")
                st.markdown(", ".join(report_result["keywords"]))

                st.markdown("#### Summary")
                st.markdown(report_result["intelligent_summary"])

            # Display anomalies in the right column
            with anomaly_col:
                st.markdown("### Prescription Analysis")
                if (
                    "prescription_anomalies" in anomaly_results
                    and anomaly_results["prescription_anomalies"]
                ):
                    for anomaly in anomaly_results["prescription_anomalies"]:
                        st.warning(f"⚠️ {anomaly}")
                else:
                    st.success("✅ No prescription anomalies detected")

# --- Auto-Refresh ---
if st.session_state.conversation_index < len(CONVERSATION_FLOW):
    st.empty()
    time.sleep(10)
    st.rerun()

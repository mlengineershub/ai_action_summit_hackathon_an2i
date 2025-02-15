import streamlit as st
import requests
import json

# Configure the base URL for the API
API_BASE_URL = "http://localhost:5000"

st.title("Medical Assistant Dashboard")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Select Function",
    [
        "Hello World",
        "Detect Prescription Anomalies",
        "Extract Ordonnance",
        "Summarize Ordonnances",
        "Search Medical Articles",
        "Generate Search Summary",
        "Generate Follow-up Questions",
        "Extract Pertinent Points",
        "Generate Search Propositions",
        "Generate Report",
    ],
)

# Hello World
if page == "Hello World":
    st.header("Hello World Test")
    if st.button("Test API Connection"):
        try:
            response = requests.get(f"{API_BASE_URL}/hello")
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the API. Make sure the Flask server is running."
            )

# Detect Prescription Anomalies
elif page == "Detect Prescription Anomalies":
    st.header("Detect Prescription Anomalies")

    doctor_prescription = st.text_area("Doctor's Prescription")
    patient_medication_history = st.text_area("Patient's Medication History")

    if st.button("Detect Anomalies"):
        if doctor_prescription and patient_medication_history:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/detect-prescription-anomalies",
                    json={
                        "doctor_prescription": doctor_prescription,
                        "patient_medication_history": patient_medication_history,
                    },
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please fill in both fields.")

# Extract Ordonnance
elif page == "Extract Ordonnance":
    st.header("Extract Ordonnance Data")

    doctor_prescription = st.text_area("Doctor's Prescription")

    if st.button("Extract Data"):
        if doctor_prescription:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/extract-ordonnance",
                    json={"doctor_prescription": doctor_prescription},
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please enter the doctor's prescription.")

# Summarize Ordonnances
elif page == "Summarize Ordonnances":
    st.header("Summarize Ordonnances")

    doctor_prescriptions = st.text_area("Doctor's Prescriptions (One per line)")

    if st.button("Generate Summary"):
        if doctor_prescriptions:
            prescriptions_list = [
                p.strip() for p in doctor_prescriptions.split("\n") if p.strip()
            ]
            try:
                response = requests.post(
                    f"{API_BASE_URL}/summarize-ordonnances",
                    json={"doctor_prescriptions": prescriptions_list},
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please enter at least one prescription.")

# Search Medical Articles
elif page == "Search Medical Articles":
    st.header("Search Medical Articles")

    query = st.text_input("Search Query")
    retmax = st.slider("Number of Results", min_value=1, max_value=20, value=5)

    if st.button("Search"):
        if query:
            try:
                response = requests.get(
                    f"{API_BASE_URL}/search-medical-articles",
                    params={"query": query, "retmax": str(retmax)},
                )
                if response.status_code == 200:
                    articles = response.json()
                    st.json(articles)

                    # Add button to fetch abstract for each article
                    if "articles" in articles:
                        for article in articles["articles"]:
                            if st.button(f"Get Abstract for {article['pmid']}"):
                                abstract_response = requests.get(
                                    f"{API_BASE_URL}/fetch-article-abstract/{article['pmid']}"
                                )
                                if abstract_response.status_code == 200:
                                    st.write(abstract_response.json()["abstract"])
                                else:
                                    st.error(
                                        f"Error fetching abstract: {abstract_response.status_code}"
                                    )
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please enter a search query.")

# Generate Search Summary
elif page == "Generate Search Summary":
    st.header("Generate Search Summary")

    patient_condition = st.text_area("Patient Condition")
    medical_articles = st.text_area("Medical Articles (JSON format)")

    if st.button("Generate Summary"):
        if patient_condition and medical_articles:
            try:
                articles_data = json.loads(medical_articles)
                response = requests.post(
                    f"{API_BASE_URL}/generate-search-summary",
                    json={
                        "patient_condition": patient_condition,
                        "medical_articles": articles_data,
                    },
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format for medical articles")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please fill in all fields.")

# Generate Follow-up Questions
elif page == "Generate Follow-up Questions":
    st.header("Generate Follow-up Questions")

    conversation = st.text_area("Conversation")

    if st.button("Generate Questions"):
        if conversation:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate-follow-up-questions",
                    json={"conversation": conversation},
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please enter the conversation.")

# Extract Pertinent Points
elif page == "Extract Pertinent Points":
    st.header("Extract Pertinent Medical Points")

    conversation = st.text_area("Conversation")
    previous_medical_history = st.text_area("Previous Medical History")

    if st.button("Extract Points"):
        if conversation and previous_medical_history:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/extract-pertinent-points",
                    json={
                        "conversation": conversation,
                        "previous_medical_history": previous_medical_history,
                    },
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please fill in all fields.")

# Generate Search Propositions
elif page == "Generate Search Propositions":
    st.header("Generate Search Propositions")

    conversation = st.text_area("Conversation")
    search_history = st.text_area("Search History")

    if st.button("Generate Propositions"):
        if conversation and search_history:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate-search-propositions",
                    json={
                        "conversation": conversation,
                        "search_history": search_history,
                    },
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please fill in all fields.")

# Generate Report
elif page == "Generate Report":
    st.header("Generate Medical Report")

    conversation = st.text_area("Conversation")
    patient_information = st.text_area("Patient Information")
    medical_history = st.text_area("Medical History")
    additional_notes = st.text_area("Additional Notes")
    additional_medical_information = st.text_area("Additional Medical Information")

    if st.button("Generate Report"):
        if all(
            [
                conversation,
                patient_information,
                medical_history,
                additional_notes,
                additional_medical_information,
            ]
        ):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate-report",
                    json={
                        "conversation": conversation,
                        "patient_information": patient_information,
                        "medical_history": medical_history,
                        "additional_notes": additional_notes,
                        "additional_medical_information": additional_medical_information,
                    },
                )
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Make sure the Flask server is running."
                )
        else:
            st.warning("Please fill in all fields.")

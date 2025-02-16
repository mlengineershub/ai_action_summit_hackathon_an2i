import streamlit as st
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial doctor message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello, I'm your medical assistant. How can I help you today?"
    })

# Create two columns: main content and search
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.subheader("Patient Consultation")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Describe your symptoms..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Simulate doctor's response based on the medical context
        # Here we'll use the existing medical analysis tools
        with st.chat_message("assistant"):
            st.markdown("Let me analyze your symptoms...")
            
            # Get follow-up questions
            questions_response = generate_follow_up_questions(
                client, 
                "\n".join(msg["content"] for msg in st.session_state.messages)
            )
            if "follow_up_questions" in questions_response and questions_response["follow_up_questions"]:
                response = questions_response["follow_up_questions"][0]  # Take the first follow-up question
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # Google Search section
    st.subheader("Medical Search")
    search_query = st.text_input("Enter medical search query")
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                search_results = summarize_google_research(client, search_query)
                st.write(search_results)

# Medical analysis sections
if len(st.session_state.messages) > 1:  # If there's any conversation beyond the initial greeting
    # Convert messages to conversation format
    full_conversation = "\n".join(f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages)
    
    # Medical Queries
    st.subheader("Suggested Medical Queries")
    queries_response = generate_search_propositions(client, full_conversation)
    if "search_propositions" in queries_response:
        for query in queries_response["search_propositions"]:
            if st.button(query):
                with st.spinner("Gathering medical knowledge..."):
                    knowledge = generate_search_summary(client, query)
                    st.write(knowledge.get("summary", "No summary available"))

    # Follow-up Questions
    st.subheader("Suggested Follow-up Questions")
    questions_response = generate_follow_up_questions(client, full_conversation)
    if "follow_up_questions" in questions_response:
        for question in questions_response["follow_up_questions"]:
            st.write("•", question)

    # Pertinent Points
    st.subheader("Pertinent Medical Points")
    points_response = extract_pertinent_medical_points(client, full_conversation)
    if "pertinent_points" in points_response:
        for point in points_response["pertinent_points"]:
            st.write("•", point)

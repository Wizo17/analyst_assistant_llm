import streamlit as st
from services.api_service import check_api_status, init_chat, send_query, download_file
from utils.logger import log_message

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 15px;
        font-size: 16px;
        background-color: #ffffff;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
    }
    .user-message {
        background-color: #f0f7ff;
    }
    .assistant-message {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }
    .chat-container {
        margin-bottom: 200px;  /* Space for input area */
        overflow-y: auto;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chats' not in st.session_state:
    st.session_state.chats = {}
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = None

# Check API status
if not check_api_status():
    st.error("API not available. Please start the API service.")
    st.stop()

def create_new_chat():
    """
    Creates a new chat session and initializes it in the session state.
    """
    session_id = init_chat()
    if session_id:
        # Generate a unique chat name
        chat_name = f"Chat {len(st.session_state.chats) + 1}"
        
        # Initialize the chat in session state
        st.session_state.chats[chat_name] = {
            "session_id": session_id,
            "history": []
        }
        
        # Set as current chat
        st.session_state.current_chat = chat_name
        log_message("INFO", f"Created new chat: {chat_name}")
        st.rerun()

# Sidebar
with st.sidebar:
    st.title("💬 Chats")
    
    # New chat button with custom styling
    if st.button("+ New Chat", type="primary", use_container_width=True):
        create_new_chat()
    
    st.markdown("---")
    
    # Chat list
    for chat_name in st.session_state.chats:
        is_selected = chat_name == st.session_state.current_chat
        if st.button(
            chat_name,
            key=f"chat_{chat_name}",
            type="secondary" if is_selected else "tertiary",
            use_container_width=True
        ):
            st.session_state.current_chat = chat_name
            st.rerun()

# Main content area
if st.session_state.current_chat:
    current_chat = st.session_state.chats[st.session_state.current_chat]
    
    # Chat history container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for entry in current_chat["history"]:
            # User message
            st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You:</b><br>{entry['query']}
                </div>
            """, unsafe_allow_html=True)
            
            # Assistant message
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <b>Assistant:</b>
                </div>
            """, unsafe_allow_html=True)
            st.json(entry['response'])
        st.markdown('</div>', unsafe_allow_html=True)

    # Fixed input area at bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    query = st.text_area("Message", height=100, placeholder="Type your message here...")
    
    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1:
        explanation_full = st.toggle("Detailed", False)
    with col2:
        output_format = "csv" if st.toggle("CSV", False) else "json"
    with col3:
        full_data = st.toggle("Full Data", False)
    with col4:
        if st.button("Send", type="primary", use_container_width=True):
            if query.strip():
                response = send_query(
                    session_id=current_chat["session_id"],
                    query=query,
                    explanation_full=explanation_full,
                    output_format=output_format,
                    full_data=full_data
                )
                if response:
                    current_chat["history"].append({
                        "query": query,
                        "response": response
                    })
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>👋 Welcome to AI Assistant</h2>
            <p>Create a new chat or select an existing one to get started.</p>
        </div>
    """, unsafe_allow_html=True)
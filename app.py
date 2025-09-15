import streamlit as st
import subprocess
import json
import tempfile
import altair as alt
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Word Frequency Analysis with AI Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #0d47a1;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        color: #4a148c;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
</style>
""", unsafe_allow_html=True)

def run_frequency_tool(file, top_n=20):
    """Run the frequency analysis tool on uploaded file."""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        
        # Run frequency tool
        result = subprocess.run(
            ["python", "frequency_tool.py", tmp_path, str(top_n)],
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        if result.returncode != 0:
            return {"error": f"Tool execution failed: {result.stderr}"}
        
        return json.loads(result.stdout)
    
    except subprocess.TimeoutExpired:
        return {"error": "Analysis timed out. Please try with a smaller document."}
    except json.JSONDecodeError:
        return {"error": "Invalid response from frequency tool."}
    except Exception as e:
        return {"error": f"Error running frequency tool: {str(e)}"}

def query_ollama(prompt: str, model: str = "llama2"):
    """Query Ollama API for AI responses."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate", 
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("response", "No response received from AI.")
        else:
            return f"Error: Ollama API returned status code {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Please make sure Ollama is running on localhost:11434"
    except requests.exceptions.Timeout:
        return "Error: Request to Ollama timed out."
    except Exception as e:
        return f"Error querying Ollama: {str(e)}"

def create_frequency_chart(data):
    """Create an interactive bar chart using Altair."""
    if not data or "error" in data[0]:
        return None
    
    df = pd.DataFrame(data)
    df = df.head(20)  # Limit to top 20 for better visualization
    
    chart = alt.Chart(df).mark_bar(
        color='#1f77b4',
        cornerRadius=4
    ).encode(
        x=alt.X('word:N', sort='-y', title='Words'),
        y=alt.Y('count:Q', title='Frequency'),
        tooltip=['word', 'count']
    ).properties(
        width=600,
        height=400,
        title="Top 20 Most Frequent Words"
    ).interactive()
    
    return chart

def create_matplotlib_chart(data):
    """Create a matplotlib bar chart as fallback."""
    if not data or "error" in data[0]:
        return None
    
    words = [item['word'] for item in data[:20]]
    counts = [item['count'] for item in data[:20]]
    
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color='#1f77b4', alpha=0.7)
    plt.title('Top 20 Most Frequent Words', fontsize=16, fontweight='bold')
    plt.xlabel('Words', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return plt

# Main UI
st.markdown('<h1 class="main-header">📊 Word Frequency Analysis with AI Agent</h1>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Top N words slider
    top_n = st.slider("Number of top words to analyze", 5, 100, 20)
    
    # Ollama model selection
    ollama_model = st.selectbox(
        "Select Ollama Model",
        ["llama3.1", "qwen3:4b",],
        help="Make sure the selected model is available in your Ollama installation"
    )
    
    # Ollama connection test
    if st.button("Test Ollama Connection"):
        with st.spinner("Testing connection..."):
            test_response = query_ollama("Hello, are you working?", ollama_model)
            if "Error" in test_response:
                st.error(test_response)
            else:
                st.success("Ollama connection successful!")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="section-header">📁 Upload Document</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX, or TXT file",
        type=["pdf", "docx", "txt"],
        help="Upload a document to analyze word frequency distribution"
    )

with col2:
    st.markdown('<h2 class="section-header">ℹ️ About</h2>', unsafe_allow_html=True)
    st.info("""
    This app analyzes word frequency in your documents and provides an AI-powered chat interface to discuss the results.
    
    **Features:**
    - Extract text from PDF, DOCX, TXT files
    - Calculate word frequency statistics
    - Interactive visualizations
    - AI chat powered by Ollama
    """)

if uploaded_file:
    st.markdown('<h2 class="section-header">📈 Analysis Results</h2>', unsafe_allow_html=True)
    
    # Show file info
    st.info(f"**File:** {uploaded_file.name} | **Size:** {uploaded_file.size:,} bytes")
    
    # Run frequency analysis
    with st.spinner("Analyzing document..."):
        freq_data = run_frequency_tool(uploaded_file, top_n)
    
    if "error" in str(freq_data):
        st.error(f"Analysis failed: {freq_data}")
    else:
        # Display results in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart", "📋 Table", "📄 JSON", "💬 AI Chat"])
        
        with tab1:
            st.markdown("### Interactive Bar Chart")
            chart = create_frequency_chart(freq_data)
            if chart:
                st.altair_chart(chart, use_container_width=True)
            else:
                st.error("Could not create chart from the data.")
        
        with tab2:
            st.markdown("### Frequency Table")
            if freq_data and not ("error" in str(freq_data)):
                df = pd.DataFrame(freq_data)
                df['rank'] = range(1, len(df) + 1)
                df = df[['rank', 'word', 'count']]
                st.dataframe(df, use_container_width=True)
            else:
                st.error("No data available for table display.")
        
        with tab3:
            st.markdown("### Raw JSON Output")
            st.json(freq_data)
        
        with tab4:
            st.markdown("### AI Chat Assistant")
            st.markdown("Ask questions about the document analysis or word frequency results.")
            
            # Initialize chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message ai-message"><strong>AI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input("Type your question:", key="chat_input")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Send", type="primary"):
                    if user_input:
                        # Add user message to history
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        
                        # Prepare context for AI
                        context = f"""
                        Document Analysis Results:
                        - File: {uploaded_file.name}
                        - Top {top_n} most frequent words: {json.dumps(freq_data, indent=2)}
                        
                        User Question: {user_input}
                        
                        Please provide a helpful response about the word frequency analysis or answer questions about the document.
                        """
                        
                        # Get AI response
                        with st.spinner("AI is thinking..."):
                            ai_response = query_ollama(context, ollama_model)
                        
                        # Add AI response to history
                        st.session_state.chat_history.append({"role": "ai", "content": ai_response})
                        
                        # Rerun to show new messages
                        st.rerun()
            
            with col2:
                if st.button("Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()

else:
    st.markdown("""
    ### Welcome to the Word Frequency Analysis App!
    
    **To get started:**
    1. Upload a PDF, DOCX, or TXT file using the file uploader above
    2. Adjust the number of top words to analyze using the slider in the sidebar
    3. View the frequency analysis results in different formats
    4. Chat with the AI assistant about your document
    
    **Supported file formats:**
    - PDF files (.pdf)
    - Microsoft Word documents (.docx)
    - Plain text files (.txt)
    """)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and powered by Ollama AI")

import streamlit as st
import asyncio
import sys
import os
import random
from dotenv import load_dotenv
import time

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.research_assistant import ResearchAssistant

# Configure the Streamlit page
st.set_page_config(
    page_title="AutoResearch",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #0066cc 0%, #0044aa 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .research-section {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .paper-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #0066cc;
    }
    .paper-title {
        color: #0066cc;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .paper-metadata {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .paper-summary {
        background-color: white;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .status-message {
        padding: 1rem;
        border-radius: 6px;
        background-color: #e6f3ff;
        margin-bottom: 1rem;
    }
    .synthesis-section {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def get_progress_message() -> str:
    """Get a random progress message."""
    messages = [
        "🔍 Exploring academic databases...",
        "📊 Analyzing research patterns...",
        "🧠 Processing scholarly insights...",
        "📑 Extracting key findings...",
        "🌟 Discovering breakthrough research...",
        "🔄 Synthesizing information...",
        "📚 Diving deep into the literature...",
        "🎯 Focusing on relevant papers...",
        "💡 Gathering innovative insights...",
        "🌐 Connecting research threads..."
    ]
    return random.choice(messages)

def init_session_state():
    if 'research_assistant' not in st.session_state:
        try:
            st.session_state.research_assistant = ResearchAssistant()
        except Exception as e:
            st.error(f"Error initializing Research Assistant: {str(e)}")
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None

def main():
    st.markdown("""
        <div class="main-header">
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>AutoResearch</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>AI-Powered Academic Research Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### Research Settings")
        max_papers = st.slider("Maximum Papers", 1, 20, 5)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        AutoResearch helps you:
        - Find relevant academic papers
        - Generate summaries
        - Analyze research trends
        - Suggest future directions
        """)

    # Main content
    st.markdown('<div class="research-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 Research Topic")
    topic = st.text_input("Enter your research topic")
    
    if st.button("Start Research", type="primary"):
        if topic:
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            results_placeholder = st.empty()
            
            with st.spinner("Researching..."):
                try:
                    start_time = time.time()
                    last_update = start_time
                    
                    while 'research_results' not in st.session_state or not st.session_state.research_results:
                        if time.time() - last_update >= 2:
                            progress_message = get_progress_message()
                            status_placeholder.markdown(f'<div class="status-message">{progress_message}</div>', unsafe_allow_html=True)
                            last_update = time.time()
                        
                        try:
                            results = asyncio.run(
                                st.session_state.research_assistant.research_topic(
                                    topic, 
                                    max_papers=max_papers
                                )
                            )
                            st.session_state.research_results = results
                            break
                        except Exception as e:
                            if "429" not in str(e):  # If not a rate limit error
                                raise
                            time.sleep(2)
                    
                    if st.session_state.research_results:
                        results = st.session_state.research_results
                        
                        # Clear progress message
                        status_placeholder.empty()
                        
                        # Show results
                        with results_placeholder.container():
                            st.success("✨ Research Complete!")
                            
                            # Display synthesis if available
                            if results.get("synthesis"):
                                st.markdown('<div class="synthesis-section">', unsafe_allow_html=True)
                                st.markdown("### 📊 Research Synthesis")
                                st.markdown(results["synthesis"])
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown("### 📚 Papers Found")
                            for i, paper in enumerate(results['papers'], 1):
                                st.markdown('<div class="paper-card">', unsafe_allow_html=True)
                                
                                # Paper title and metadata
                                st.markdown(f"#### {paper['title']}")
                                col1, col2 = st.columns([2,1])
                                
                                with col1:
                                    st.markdown(f"**Authors:** {', '.join(a['name'] for a in paper['authors'])}")
                                    st.markdown(f"**Year:** {paper.get('year', 'N/A')}")
                                
                                with col2:
                                    if paper.get('url'):
                                        st.markdown(f"🔗 [Read Paper]({paper['url']})")
                                    if paper.get('citation_count') is not None:
                                        st.markdown(f"📚 Citations: {paper['citation_count']}")
                                
                                # Paper summary
                                st.markdown("**Summary:**")
                                st.markdown('<div class="paper-summary">', unsafe_allow_html=True)
                                st.markdown(paper['summary'])
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"Error during research: {str(e)}")
                    st.error("Please try again in a few moments.")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

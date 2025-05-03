import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

def check_gemini_key(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello")
        return True, "✅ Gemini API key is valid"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

st.set_page_config(page_title="Configuration Check", page_icon="⚙️")

st.markdown("""
# Configuration Check
Check the status of your API keys and configuration.
""")

# Load current configuration
load_dotenv()

# Gemini API Key
st.markdown("### Google Gemini API Key")
gemini_key = os.getenv('GOOGLE_API_KEY', '')
new_gemini_key = st.text_input(
    "Gemini API Key",
    value=gemini_key,
    type="password"
)

if st.button("Test Configuration"):
    with st.spinner("Testing API key..."):
        # Test Gemini
        status, message = check_gemini_key(new_gemini_key)
        st.markdown(f"**Gemini API:** {message}")

        if status:
            # Update .env file
            with open('.env', 'w') as f:
                f.write(f"GOOGLE_API_KEY={new_gemini_key}\n")
                f.write(f"GROBID_SERVER=http://localhost:8070\n")
            st.success("Configuration updated successfully!")
        else:
            st.error("Please fix the configuration issues above.")

st.markdown("""
### Help
1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Copy the API key and paste it above
3. Click "Test Configuration" to verify and save the key
""")

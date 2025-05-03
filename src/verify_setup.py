import os
from dotenv import load_dotenv
import requests
from src.semantic_scholar import SemanticScholarAPI
from langchain_openai import OpenAI

def verify_api_keys():
    print("Verifying API keys and connections...")
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("❌ OpenAI API key not found in .env file")
        return False
    
    try:
        llm = OpenAI(api_key=openai_key)
        # Simple test completion
        response = llm.invoke("Say 'API test successful'")
        print("✓ OpenAI API key is valid and working")
    except Exception as e:
        print(f"❌ OpenAI API key is invalid or there was an error: {str(e)}")
        return False

    # Check Semantic Scholar API key
    semantic_scholar_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
    if not semantic_scholar_key:
        print("❌ Semantic Scholar API key not found in .env file")
        return False
    
    try:
        api = SemanticScholarAPI(semantic_scholar_key)
        # Test search with minimal results
        test_response = api.search_papers("test", limit=1)
        print("✓ Semantic Scholar API key is valid and working")
    except Exception as e:
        print(f"❌ Semantic Scholar API key is invalid or there was an error: {str(e)}")
        return False

    print("\n✓ All API keys are valid and working!")
    return True

if __name__ == "__main__":
    print("API Key Verification Tool")
    print("-----------------------")
    print("This tool will verify your API keys are properly configured.")
    print("Please ensure you have copied .env.template to .env and filled in your API keys.")
    print()
    
    verify_api_keys()

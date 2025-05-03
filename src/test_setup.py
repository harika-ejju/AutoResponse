from src.config import Config
from src.research_assistant import ResearchAssistant

def test_setup():
    try:
        # Test configuration loading
        config = Config()
        print("✓ Configuration loaded successfully")
        
        # Test research assistant initialization
        assistant = ResearchAssistant()
        print("✓ Research Assistant initialized successfully")
        
        return True
    except Exception as e:
        print(f"✗ Setup test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing AutoResearch setup...")
    test_setup()

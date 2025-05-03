from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.semantic_scholar_api_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
        
        # Grobid Settings
        self.grobid_server = os.getenv('GROBID_SERVER', 'http://localhost:8070')
        
        # FAISS Settings
        self.embedding_dimension = 1536  # Default for text-embedding-ada-002
        self.index_path = 'models/faiss_index'
        
        # Validate configuration
        self.validate_config()
    
    def validate_config(self):
        """Validate that all required configuration is present."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.semantic_scholar_api_key:
            raise ValueError("SEMANTIC_SCHOLAR_API_KEY is required")

import requests
import time
from typing import Dict, List, Optional
import logging
import urllib.parse

class SemanticScholarAPI:
    def __init__(self, api_key: str = None):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["x-api-key"] = api_key
        
        self.rate_limit_delay = 1  # Delay between requests in seconds

    def search_papers(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for papers matching the query."""
        endpoint = f"{self.base_url}/paper/search"
        
        # Define the fields we want to retrieve
        fields = [
            "title",
            "authors",
            "year",
            "abstract",
            "url",
            "citationCount",
            "venue",
            "publicationTypes",
            "openAccessPdf"
        ]
        
        params = {
            "query": query,
            "limit": limit,
            "fields": ",".join(fields)
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Error searching papers: {str(e)}")
            if response.status_code == 400:
                logging.error(f"API Response: {response.text}")
            raise

    def get_paper_details(self, paper_id: str) -> Dict:
        """Get detailed information about a specific paper."""
        endpoint = f"{self.base_url}/paper/{paper_id}"
        
        fields = [
            "title",
            "authors",
            "year",
            "abstract",
            "url",
            "citationCount",
            "venue",
            "publicationTypes",
            "openAccessPdf"
        ]
        
        params = {
            "fields": ",".join(fields)
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            return response.json()
        except Exception as e:
            logging.error(f"Error getting paper details: {e}")
            raise


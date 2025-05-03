import fitz  # PyMuPDF
import requests
import logging
from typing import Dict, List, Optional
import os
import json

class DocumentProcessor:
    def __init__(self, grobid_server: str):
        self.grobid_server = grobid_server
        self.logger = logging.getLogger(__name__)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract raw text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            raise

    def process_with_grobid(self, pdf_path: str) -> Dict:
        """Process PDF with Grobid to extract structured information."""
        try:
            # Check if Grobid server is running
            if not self._check_grobid_server():
                raise ConnectionError("Grobid server is not available")

            # Prepare the PDF file for upload
            with open(pdf_path, 'rb') as pdf_file:
                files = {'input': pdf_file}
                
                # Make request to Grobid
                response = requests.post(
                    f"{self.grobid_server}/api/processFulltextDocument",
                    files=files
                )
                response.raise_for_status()
                
                return self._parse_grobid_response(response.text)
        except Exception as e:
            self.logger.error(f"Error processing document with Grobid: {e}")
            raise

    def _check_grobid_server(self) -> bool:
        """Check if Grobid server is running."""
        try:
            response = requests.get(f"{self.grobid_server}/api/isalive")
            return response.status_code == 200
        except:
            return False

    def _parse_grobid_response(self, response_text: str) -> Dict:
        """Parse Grobid XML response into structured data."""
        # This is a simplified parser - in practice, you'd want to use
        # a proper XML parser to extract detailed information
        structured_data = {
            'title': '',
            'abstract': '',
            'authors': [],
            'references': [],
            'body_text': ''
        }
        # Implementation would parse XML response and populate structured_data
        return structured_data

    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract metadata from PDF."""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            return metadata
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {e}")
            raise


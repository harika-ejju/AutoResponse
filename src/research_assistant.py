import os
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from src.semantic_scholar import SemanticScholarAPI
from src.cache_manager import CacheManager
import asyncio
import json
from datetime import datetime, timedelta

class ResearchAssistant:
    def __init__(self):
        """Initialize the research assistant."""
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize cache
        self.cache = CacheManager()
        
        # Initialize Gemini
        self.gemini_key = os.getenv('GOOGLE_API_KEY')
        if not self.gemini_key:
            raise ValueError("Gemini API key not found. Please set GOOGLE_API_KEY in .env file")
            
        # Configure Gemini API
        genai.configure(api_key=self.gemini_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Initialize Semantic Scholar API
        self.semantic_scholar = SemanticScholarAPI()
        
        # Rate limiting settings
        self.last_api_call = datetime.now()
        self.min_delay = 3  # Minimum delay between API calls in seconds
        
        self.logger.info("Research Assistant initialized successfully")

    async def _wait_for_rate_limit(self):
        """Wait if needed to respect rate limits."""
        now = datetime.now()
        elapsed = (now - self.last_api_call).total_seconds()
        if elapsed < self.min_delay:
            await asyncio.sleep(self.min_delay - elapsed)
        self.last_api_call = datetime.now()

    async def _generate_content_with_retry(self, prompt: str, cache_key: str = None, max_retries: int = 3) -> str:
        """Generate content with retry logic, rate limiting, and caching."""
        if cache_key:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result

        for attempt in range(max_retries):
            try:
                await self._wait_for_rate_limit()
                response = self.model.generate_content(prompt)
                result = response.text
                
                if cache_key:
                    self.cache.set(cache_key, result)
                
                return result
            except Exception as e:
                if "429" in str(e):  # Rate limit error
                    retry_delay = min(2 ** attempt * 5, 30)  # Exponential backoff
                    self.logger.warning(f"Rate limit hit, waiting {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    self.logger.error(f"Error generating content: {e}")
                    if attempt == max_retries - 1:
                        return f"Error: Failed to generate content after {max_retries} attempts."
        return "Error: Maximum retries exceeded."

    async def research_topic(self, topic: str, max_papers: int = 5) -> Dict:
        """Conduct research on a specific topic."""
        # Check cache first
        cache_key = f"research_{topic}_{max_papers}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.logger.info(f"Using cached results for topic: {topic}")
            return cached_result

        try:
            self.logger.info(f"Researching topic: {topic}")
            
            # Search for papers with retries
            papers = None
            for attempt in range(3):
                try:
                    papers = self.semantic_scholar.search_papers(topic, limit=max_papers)
                    break
                except Exception as e:
                    if "429" in str(e):
                        retry_delay = min(2 ** attempt * 5, 30)
                        self.logger.warning(f"Rate limit hit, waiting {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        raise

            if not papers:
                self.logger.warning(f"No papers found for topic: {topic}")
                return {
                    "topic": topic,
                    "papers": [],
                    "error": "No papers found for the given topic",
                    "synthesis": ""
                }
            
            research_results = {
                "topic": topic,
                "papers": [],
                "synthesis": "",
                "stats": {
                    "total_papers": len(papers),
                    "successful_summaries": 0,
                    "failed_summaries": 0
                }
            }
            
            # Process papers
            for i, paper in enumerate(papers, 1):
                self.logger.info(f"Processing paper {i}/{len(papers)}: {paper.get('title', 'Unknown')}")
                paper_result = await self._process_paper(paper)
                research_results["papers"].append(paper_result)
                
                if "error" not in paper_result:
                    research_results["stats"]["successful_summaries"] += 1
                else:
                    research_results["stats"]["failed_summaries"] += 1
                
                # Add delay between papers
                if i < len(papers):
                    await asyncio.sleep(self.min_delay)
            
            # Generate synthesis only if we have at least one successful summary
            if research_results["stats"]["successful_summaries"] > 0:
                synthesis_prompt = f"""
                Based on the following papers about {topic}, provide a synthesis of the field and suggest future research directions:
                
                Papers:
                {json.dumps([{
                    'title': p['title'],
                    'year': p.get('year', 'N/A'),
                    'key_points': p.get('summary', '')[:200] + '...'
                } for p in research_results["papers"] if 'error' not in p], indent=2)}
                
                Please provide:
                1. Overview of Current Research
                2. Key Themes and Patterns
                3. Research Gaps
                4. Future Research Directions
                
                Format the response with clear sections and bullet points.
                """
                
                synthesis_cache_key = f"synthesis_{topic}"
                research_results["synthesis"] = await self._generate_content_with_retry(
                    synthesis_prompt,
                    cache_key=synthesis_cache_key
                )
            
            # Cache the results
            self.cache.set(cache_key, research_results)
            
            return research_results
            
        except Exception as e:
            self.logger.error(f"Error in research process: {e}")
            raise

    async def _process_paper(self, paper: Dict) -> Dict:
        """Process a single paper and extract relevant information."""
        base_result = {
            "title": paper.get("title", "Unknown Title"),
            "authors": paper.get("authors", []),
            "year": paper.get("year", "N/A"),
            "url": paper.get("url", ""),
            "pdf_url": paper.get("openAccessPdf", {}).get("url", ""),
            "venue": paper.get("venue", ""),
            "citation_count": paper.get("citationCount", 0),
            "publication_types": paper.get("publicationTypes", [])
        }
        
        try:
            # Check cache first
            cache_key = f"paper_{paper.get('paperId', '')}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return {**base_result, **cached_result}

            # Prepare paper information for summary
            title = paper.get("title", "")
            authors = [a.get('name', '') for a in paper.get('authors', [])]
            year = paper.get('year', 'N/A')
            abstract = paper.get('abstract', 'No abstract available')
            
            prompt = f"""
            Analyze this research paper and provide a structured summary:

            Title: {title}
            Authors: {', '.join(authors)}
            Year: {year}
            Abstract: {abstract}

            Provide a structured analysis with these sections:
            1. Main Contributions
            2. Methodology
            3. Key Findings
            4. Future Research Directions

            Format each section with bullet points for clarity.
            Keep the summary concise but comprehensive.
            """
            
            summary = await self._generate_content_with_retry(prompt, cache_key=cache_key)
            base_result["summary"] = summary
            
            # Cache the result
            self.cache.set(cache_key, {"summary": summary})
            
            return base_result
            
        except Exception as e:
            self.logger.error(f"Error processing paper: {e}")
            base_result["error"] = str(e)
            base_result["summary"] = "Failed to generate summary"
            return base_result


# AutoResearch

AI-powered academic research assistant using GPT-4, LangChain, and Semantic Scholar API.

## Quick Start with Docker

1. Create a `.env` file with your API keys:
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

2. Build and run with Docker:
```bash
./build_and_run.sh
```

3. Access the application at http://localhost:8501

## Manual Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys in `.env` file

4. Run the application:
```bash
streamlit run frontend/app.py
```

## Project Structure

```
AutoResearch/
├── frontend/          # Streamlit frontend
├── src/              # Core application code
├── cache/            # Cache directory
├── data/             # Data directory
├── models/           # Model files
├── Dockerfile        # Docker configuration
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Features

- Research paper search and analysis
- AI-powered paper summarization
- Research synthesis generation
- Citation analysis
- Cached results for better performance

## Development

To build and run in development mode:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run the application
streamlit run frontend/app.py
```

## Docker Commands

```bash
# Build the image
docker build -t autoresearch .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## Cache Management

The application caches research results and summaries in the `cache/` directory. To clear the cache:

```bash
# Remove cache files
rm -rf cache/*

# Or using Docker
docker-compose down
docker volume rm autoresearch_cache
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
# AutoResponse
# AutoResponse

import asyncio
from src.research_assistant import ResearchAssistant

async def main():
    try:
        print("Initializing Research Assistant...")
        assistant = ResearchAssistant()
        
        # Test with a sample topic
        topic = "GPT-4 and Research Automation"
        print(f"\nResearching topic: {topic}")
        
        results = await assistant.research_topic(topic, max_papers=3)
        
        print("\nResearch Results:")
        print(f"Topic: {results['topic']}")
        print("\nPapers found:")
        for i, paper in enumerate(results['papers'], 1):
            print(f"\n{i}. {paper['title']} ({paper.get('year', 'N/A')})")
            print(f"Authors: {', '.join(a['name'] for a in paper['authors'])}")
            print(f"Summary: {paper['summary']}")
        
    except Exception as e:
        print(f"Error in demo: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

"""Demo script to test the Agentic RAG System locally"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_rag_workflow():
    """Test the RAG workflow with sample queries"""
    
    # Import the RAG processor
    try:
        from src.agent import rag_processor
        from src.tools import RAGDeps
        
        print("🚀 Starting Agentic RAG System Demo")
        print("=" * 50)
        
        # Initialize dependencies
        deps = RAGDeps()
        
        # Test queries
        test_queries = [
            "What is machine learning?",
            "Calculate 25 * 4 + 10",
            "What are the latest AI developments?",
            "Compare supervised vs unsupervised learning"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test Query {i}: {query}")
            print("-" * 30)
            
            try:
                # Process query through 12-step workflow
                result = await rag_processor.process_query_workflow(query, deps)
                
                # Display results
                print(f"✅ Answer: {result.answer}")
                print(f"🎯 Confidence: {result.confidence:.1%}")
                print(f"📚 Sources: {', '.join(result.sources)}")
                
                if result.metadata.get('grading_scores'):
                    scores = result.metadata['grading_scores']
                    print(f"📊 Quality Scores:")
                    print(f"   Relevancy: {scores.relevancy_score:.1%}")
                    print(f"   Faithfulness: {scores.faithfulness_score:.1%}")
                    print(f"   Context: {scores.context_quality_score:.1%}")
                    print(f"   Coherence: {scores.coherence_score:.1%}")
                
                print(f"🔄 Method: {result.metadata.get('retrieval_method', 'unknown')}")
                print(f"🔁 Rewrites: {result.metadata.get('query_rewrites', 0)}")
                
            except Exception as e:
                print(f"❌ Error processing query: {str(e)}")
            
            print("\n" + "=" * 50)
        
        print("🎉 Demo completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure to run this from the agent directory with:")
        print("cd agent && python demo.py")
    
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   {var}")
        print("\nPlease set these in your .env file")
        exit(1)
    
    # Run the demo
    asyncio.run(test_rag_workflow())
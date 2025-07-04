#!/usr/bin/env python3
"""
Memory Inspection Demo

This script demonstrates how to use the memory inspection tools
to analyze the memories stored in the TradingAgents system.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from strands_agents.model_utils import get_model
from strands_agents.agents.reflector import TradingReflector
from strands_agents.default_config import DEFAULT_CONFIG
from strands_agents.tools.memory import FinancialSituationMemory
from inspect_memories import MemoryInspector


def create_sample_memories():
    """Create some sample memories for demonstration."""
    print("Creating sample memories for demonstration...")
    
    try:
        llm = get_model(provider='bedrock')
        reflector = TradingReflector(llm, DEFAULT_CONFIG)
        
        # Sample trading scenarios
        sample_scenarios = [
            {
                "state": {
                    "market_report": "NVDA technical analysis shows strong bullish breakout above $450 resistance with high volume (2x average). RSI at 65, MACD bullish crossover confirmed.",
                    "sentiment_report": "Positive sentiment across social media platforms (85% bullish) with high engagement on AI developments and earnings expectations.",
                    "news_report": "NVIDIA announced new AI chip partnerships with major cloud providers. Q3 earnings beat expectations with data center revenue up 200% YoY.",
                    "fundamentals_report": "Strong fundamentals: P/E ratio 45 (reasonable for growth), revenue growth 126% YoY, profit margins expanding from 15% to 22%.",
                    "trader_investment_plan": "FINAL TRANSACTION PROPOSAL: **BUY** - Strong technical breakout, positive sentiment, and solid fundamentals support a bullish position.",
                    "investment_debate_state": {
                        "bull_history": "Bull case: AI boom continues, data center demand strong, technical breakout confirmed with volume.",
                        "bear_history": "Bear case: High valuation concerns, potential market correction, geopolitical risks with China trade.",
                        "judge_decision": "Bullish consensus based on strong fundamentals and technical signals outweighing valuation concerns."
                    },
                    "risk_debate_state": {
                        "judge_decision": "Approved BUY with 2% position size limit due to volatility concerns and sector concentration risk."
                    }
                },
                "outcome": "Trade Result: +18% return over 2 weeks. Stock moved from $450 to $531. Excellent timing on entry, AI news catalyzed the move."
            },
            {
                "state": {
                    "market_report": "AAPL showing mixed technical signals - above 50-day MA but below 200-day MA. Volume declining, consolidation pattern forming.",
                    "sentiment_report": "Neutral sentiment (52% bullish) with investors waiting for iPhone 15 sales data and services growth metrics.",
                    "news_report": "Apple reported steady Q3 results but China sales declined 3% YoY. Services revenue growth slowing to 8% from previous 15%.",
                    "fundamentals_report": "Solid fundamentals but growth slowing: P/E 28, revenue growth 2% YoY, margins stable at 25%. Strong balance sheet.",
                    "trader_investment_plan": "FINAL TRANSACTION PROPOSAL: **HOLD** - Mixed signals suggest waiting for clearer direction before making moves.",
                    "investment_debate_state": {
                        "bull_history": "Bull case: Strong brand loyalty, services growth, potential for new product categories.",
                        "bear_history": "Bear case: China weakness, slowing growth, high valuation for current growth rate.",
                        "judge_decision": "Conservative hold approach given mixed signals and uncertain growth trajectory."
                    },
                    "risk_debate_state": {
                        "judge_decision": "Approved HOLD strategy with readiness to add on significant weakness below $170."
                    }
                },
                "outcome": "Trade Result: +4% return over 1 month. Conservative approach was appropriate given market uncertainty. Avoided potential downside."
            },
            {
                "state": {
                    "market_report": "TSLA showing bearish technical divergence - price making higher highs but RSI making lower highs. Support at $200 breaking.",
                    "sentiment_report": "Negative sentiment (70% bearish) with concerns about production issues, CEO distraction, and competitive pressure.",
                    "news_report": "Tesla reported production shortfalls, Cybertruck delays, and increased competition from traditional automakers in EV space.",
                    "fundamentals_report": "Deteriorating fundamentals: P/E 60 (high for slowing growth), revenue growth 8% YoY down from 50%, margin pressure.",
                    "trader_investment_plan": "FINAL TRANSACTION PROPOSAL: **SELL** - Multiple negative factors align suggesting significant downside risk.",
                    "investment_debate_state": {
                        "bull_history": "Bull case: EV market leader, innovation in autonomous driving, energy storage growth potential.",
                        "bear_history": "Bear case: Valuation too high, execution issues, competitive threats, regulatory concerns.",
                        "judge_decision": "Bearish consensus due to execution issues and valuation concerns outweighing long-term potential."
                    },
                    "risk_debate_state": {
                        "judge_decision": "Approved SELL recommendation with tight stop-loss if position reverses unexpectedly."
                    }
                },
                "outcome": "Trade Result: Avoided -15% loss over 3 weeks. Stock dropped from $220 to $187. Technical analysis and sentiment proved predictive."
            }
        ]
        
        # Generate reflections for each scenario
        for i, scenario in enumerate(sample_scenarios, 1):
            print(f"Processing scenario {i}...")
            reflections = reflector.reflect_on_all_components(scenario["state"], scenario["outcome"])
            print(f"✅ Generated reflections for scenario {i}")
        
        print(f"✅ Created sample memories from {len(sample_scenarios)} trading scenarios")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample memories: {e}")
        return False


def demonstrate_memory_inspection():
    """Demonstrate various memory inspection capabilities."""
    print("\n" + "=" * 60)
    print("🔍 MEMORY INSPECTION DEMONSTRATION")
    print("=" * 60)
    
    inspector = MemoryInspector()
    
    # 1. Discover collections
    print("\n1️⃣ DISCOVERING MEMORY COLLECTIONS")
    print("-" * 40)
    collections = inspector.discover_collections()
    
    if not collections:
        print("No collections found. Creating sample memories first...")
        if create_sample_memories():
            collections = inspector.discover_collections()
    
    # 2. Show collection statistics
    print("\n2️⃣ COLLECTION STATISTICS")
    print("-" * 40)
    for collection_name in collections[:3]:  # Show first 3 collections
        stats = inspector.get_collection_stats(collection_name)
        print(f"\n📊 {collection_name}:")
        print(f"   Total memories: {stats.get('total_memories', 0)}")
        print(f"   Embedding dimensions: {stats.get('embedding_dimensions', 0)}")
        print(f"   Average document length: {stats.get('avg_document_length', 0):.0f} chars")
    
    # 3. Inspect content of one collection
    if collections:
        print(f"\n3️⃣ CONTENT INSPECTION - {collections[0]}")
        print("-" * 40)
        content = inspector.inspect_collection_content(collections[0], limit=2)
        
        for i, memory in enumerate(content.get("memories", [])[:2]):
            print(f"\n📄 Memory {i+1}:")
            situation = memory.get("situation", "")[:150]
            recommendation = memory.get("recommendation", "")[:150]
            print(f"   Situation: {situation}...")
            print(f"   Recommendation: {recommendation}...")
    
    # 4. Search demonstration
    if collections:
        print(f"\n4️⃣ SEMANTIC SEARCH DEMONSTRATION")
        print("-" * 40)
        search_queries = [
            "NVDA technical analysis bullish",
            "risk management position sizing",
            "earnings beat expectations"
        ]
        
        for query in search_queries:
            print(f"\n🔍 Searching: '{query}'")
            results = inspector.search_memories(collections[0], query, n_results=2)
            
            for i, result in enumerate(results.get("results", [])[:1]):  # Show top result
                similarity = result.get("similarity_score", 0)
                situation = result.get("matched_situation", "")[:100]
                print(f"   Top result (similarity: {similarity:.3f}): {situation}...")
    
    # 5. Pattern analysis
    if collections:
        print(f"\n5️⃣ PATTERN ANALYSIS - {collections[0]}")
        print("-" * 40)
        analysis = inspector.analyze_memory_patterns(collections[0])
        
        patterns = analysis.get("patterns", {})
        if "common_situation_words" in patterns:
            print("   Top situation words:")
            for word, freq in patterns["common_situation_words"][:5]:
                print(f"     {word}: {freq} times")
    
    # 6. Collection comparison
    print(f"\n6️⃣ COLLECTION COMPARISON")
    print("-" * 40)
    comparison = inspector.compare_collections(collections[:3])
    summary = comparison.get("summary", {})
    print(f"   Total collections: {summary.get('total_collections', 0)}")
    print(f"   Total memories: {summary.get('total_memories_across_all', 0)}")
    print(f"   Average per collection: {summary.get('avg_memories_per_collection', 0):.1f}")


def demonstrate_simple_viewer():
    """Demonstrate the simple memory viewer."""
    print("\n" + "=" * 60)
    print("👁️ SIMPLE MEMORY VIEWER DEMONSTRATION")
    print("=" * 60)
    
    from view_memories import view_all_collections, search_memories
    
    # Show all collections
    print("\n📋 All Collections Overview:")
    view_all_collections()
    
    # Demonstrate search
    print("\n🔍 Search Example:")
    try:
        search_memories("trader_memory", "technical analysis", n_results=2)
    except Exception as e:
        print(f"Search example skipped: {e}")


def show_usage_examples():
    """Show practical usage examples."""
    print("\n" + "=" * 60)
    print("💡 PRACTICAL USAGE EXAMPLES")
    print("=" * 60)
    
    print("\n🔧 Command Line Usage:")
    print("# Quick overview of all collections")
    print("python view_memories.py")
    print()
    print("# View detailed content of a specific collection")
    print("python view_memories.py view trader_memory")
    print()
    print("# Search for specific trading scenarios")
    print("python view_memories.py search bull_memory 'NVDA technical analysis'")
    print()
    print("# Analyze patterns in memories")
    print("python view_memories.py analyze risk_manager_memory")
    print()
    print("# Export memories to JSON file")
    print("python view_memories.py export trader_memory my_export.json")
    
    print("\n🐍 Python Code Usage:")
    print("""
# Import the inspector
from inspect_memories import MemoryInspector

# Create inspector instance
inspector = MemoryInspector()

# Discover all collections
collections = inspector.discover_collections()

# Get detailed stats
stats = inspector.get_collection_stats('trader_memory')

# Search memories
results = inspector.search_memories('trader_memory', 'NVDA analysis', n_results=5)

# Generate comprehensive report
report_file = inspector.generate_report('my_memory_report.json')
""")
    
    print("\n📊 Analysis Use Cases:")
    print("• Monitor learning progress - see how many memories each component has")
    print("• Debug reflection quality - inspect actual stored reflections")
    print("• Find similar scenarios - search for past trading situations")
    print("• Export for analysis - get data for external analysis tools")
    print("• Pattern discovery - find common themes in successful/failed trades")


def main():
    """Main demonstration function."""
    print("🎯 TradingAgents Memory Inspection Tools Demo")
    print("=" * 60)
    
    try:
        # Create sample data if needed
        print("Setting up demonstration environment...")
        create_sample_memories()
        
        # Run demonstrations
        demonstrate_memory_inspection()
        demonstrate_simple_viewer()
        show_usage_examples()
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("\nYou now have comprehensive tools to inspect and analyze")
        print("the memories stored in your TradingAgents system!")
        print("\nNext steps:")
        print("1. Use 'python view_memories.py' for quick inspection")
        print("2. Use 'python inspect_memories.py --interactive' for detailed analysis")
        print("3. Export memories for external analysis with the export functions")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

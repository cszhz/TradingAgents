#!/usr/bin/env python3
"""
Simple CLI for TradingAgents

A simplified command-line interface for running TradingAgents analysis.
This provides a straightforward way to analyze stocks without the complex UI.
"""

import argparse
import sys
from datetime import datetime
from model_utils import get_model
from default_config import DEFAULT_CONFIG
from graph.trading_graph import TradingAgentsGraph


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="TradingAgents: Multi-Agent Trading Analysis Framework"
    )
    
    parser.add_argument(
        "ticker",
        help="Stock ticker symbol to analyze (e.g., AAPL, TSLA, SPY)"
    )
    
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Analysis date in YYYY-MM-DD format (default: today)"
    )
    
    parser.add_argument(
        "--online",
        action="store_true",
        help="Use real-time data instead of cached data"
    )
    
    parser.add_argument(
        "--provider",
        choices=["bedrock", "openai"],
        default="bedrock",
        help="LLM provider to use (default: bedrock)"
    )
    
    parser.add_argument(
        "--deep-model",
        default=DEFAULT_CONFIG["deep_think_llm"],
        help="Model for complex reasoning tasks"
    )
    
    parser.add_argument(
        "--quick-model", 
        default=DEFAULT_CONFIG["quick_think_llm"],
        help="Model for quick analysis tasks"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Starting TradingAgents analysis for {args.ticker} on {args.date}")
    print(f"📊 Using {'real-time' if args.online else 'cached'} data")
    print(f"🤖 LLM Provider: {args.provider}")
    print("-" * 60)
    
    try:
        # Initialize models
        print("Initializing language models...")
        llm = get_model(
            provider=args.provider,
            model_id=args.deep_model,
            thinking=True
        )
        
        quick_llm = get_model(
            provider=args.provider,
            model_id=args.quick_model,
            thinking=False
        )
        
        # Create configuration
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = args.provider
        config["online_tools"] = args.online
        
        # Initialize TradingAgents graph
        print("Initializing TradingAgents framework...")
        graph = TradingAgentsGraph(
            llm=llm,
            quick_llm=quick_llm,
            online=args.online,
            config=config
        )
        
        # Run analysis
        print(f"Running complete analysis for {args.ticker}...")
        final_state, final_decision = graph.propagate(args.ticker, args.date)
        
        # Display results
        print("\n" + "=" * 60)
        print("📈 ANALYSIS COMPLETE")
        print("=" * 60)
        
        print(f"\n🎯 Final Trading Decision:")
        print("-" * 30)
        print(final_decision)
        
        print(f"\n📁 Results saved to: {config['results_dir']}/{args.ticker}_{args.date}")
        
        # Display summary
        print(f"\n📊 Analysis Summary:")
        print(f"   • Company: {final_state['company']}")
        print(f"   • Date: {final_state['trade_date']}")
        print(f"   • Market Analysis: ✅")
        print(f"   • News Analysis: ✅") 
        print(f"   • Research Debate: ✅")
        print(f"   • Trading Decision: ✅")
        
        print("\n✨ Analysis completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
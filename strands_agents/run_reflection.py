import sys
import os
from pathlib import Path
from model_utils import get_model
# Add the parent directory to Python path so strands_agents can be imported
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
from graph.trading_graph import TradingAgentsGraph
from strands_agents.default_config import DEFAULT_CONFIG

    


def main():
    """
    Main function demonstrating TradingAgents with reflection capabilities.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="TradingAgents Memory Inspector")
    parser.add_argument("--company", "-c", help="股票代码，如:‘AMZN’")
    parser.add_argument("--trade_date", "-d", help="截止的交易日 格式 YYYY-MM-DD")
    args = parser.parse_args()
    print("TradingAgents with Strands - Reflection Demo")
    print("=" * 50)

    # Get the model
    llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],model_id=DEFAULT_CONFIG["deep_think_llm"])
    quick_llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],model_id=DEFAULT_CONFIG["quick_think_llm"],max_tokens=10000)

    # Create trading system with reflection capabilities
    ta = TradingAgentsGraph(llm=llm,quick_llm=quick_llm, online=False)
    
    # Run trading analysis
    company = args.company
    trade_date = args.trade_date
   
    # Example 1: Successful trade reflection
    print("\n--- Example 1: Reflecting on a Successful Trade ---")
    successful_outcome = (
        "Trade Result: +12% return over 2 weeks. "
        "Stock moved from $180 to $201.60. "
        "Excellent timing on entry, strong fundamentals confirmed."
    )
    
    success_reflections = ta.reflection_step(company, trade_date, successful_outcome)
    print("✅ Successful trade reflection completed and stored in memory.")

if __name__ == "__main__":
    main()

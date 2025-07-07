import sys
import os
from pathlib import Path
from model_utils import get_model
# Add the parent directory to Python path so strands_agents can be imported
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
from graph.trading_graph import TradingAgentsGraph
from strands_agents.default_config import DEFAULT_CONFIG
import os,base64
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
)
logger = logging.getLogger(__name__)



def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TradingAgents Memory Inspector")
    parser.add_argument("--company", "-c", help="股票代码，如:‘AMZN’")
    parser.add_argument("--trade_date", "-d", help="截止的交易日 格式 YYYY-MM-DD")
    parser.add_argument("--begin_step", "-s", type=int, default=1)    
    parser.add_argument("--end_step", "-e", type=int, default=99)    
    parser.add_argument("--online", "-o", type=bool, default=True)  
    args = parser.parse_args()
    
    print("TradingAgents with Strands - Decision Demo")
    print("=" * 50)

    # Get the model
    llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],model_id=DEFAULT_CONFIG["deep_think_llm"],max_tokens=16000)
    quick_llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],thinking=False, model_id=DEFAULT_CONFIG["quick_think_llm"],max_tokens=10000)

    # Create trading system with reflection capabilities
    ta = TradingAgentsGraph(llm=llm,quick_llm=quick_llm, online=args.online)
    
    # Run trading analysis
    company = args.company
    trade_date = args.trade_date
    begin_step = args.begin_step
    end_step = args.end_step
    
    print(f"Analyzing {company} for {trade_date}...")
    final_decision = ta.run(company, trade_date,begin_step,end_step)
    
    print(f"\nFinal Trading Decision:{final_decision}")

if __name__ == "__main__":
    main()

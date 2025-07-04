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
from strands.telemetry import StrandsTelemetry
from dotenv import load_dotenv
load_dotenv()

public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
langfuse_endpoint =  os.environ.get("LANGFUSE_HOST")
# Set up endpoint
if public_key and secret_key and langfuse_endpoint:
    print("-------------------start trace-------------------")
    otel_endpoint = langfuse_endpoint + "/api/public/otel/v1/traces"
    auth_token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TradingAgents Memory Inspector")
    parser.add_argument("--company", "-c", help="股票代码，如:‘AMZN’")
    parser.add_argument("--trade_date", "-d", help="截止的交易日 格式 YYYY-MM-DD")
    args = parser.parse_args()
    
    print("TradingAgents with Strands - Decision Demo")
    print("=" * 50)

    # Get the model
    llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],model_id=DEFAULT_CONFIG["deep_think_llm"],max_tokens=10000)
    quick_llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],thinking=False, model_id=DEFAULT_CONFIG["quick_think_llm"],max_tokens=10000)

    # Create trading system with reflection capabilities
    ta = TradingAgentsGraph(llm=llm,quick_llm=quick_llm, online=False)
    
    # Run trading analysis
    company = args.company
    trade_date = args.trade_date
    
    print(f"Analyzing {company} for {trade_date}...")
    final_decision = ta.run(company, trade_date)
    
    print(f"\nFinal Trading Decision:{final_decision}")

if __name__ == "__main__":
    main()

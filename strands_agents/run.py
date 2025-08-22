import sys
import os
from pathlib import Path
from model_utils import get_model,save_as_file,read_file
# Add the parent directory to Python path so strands_agents can be imported
#parent_dir = Path(__file__).parent.parent
parent_dir = "/home/ubuntu/TradingAgents"
sys.path.insert(0, str(parent_dir))
#from graph.trading_graph import TradingAgentsGraph
from default_config import DEFAULT_CONFIG
import os,base64
import logging

from strands_agents.agents import (
    create_market_analyst,
    create_news_analyst,
    create_research_manager,
    create_bear_researcher,
    create_bull_researcher,
    create_trader,
    ConversationSwarm,
)

from dotenv import load_dotenv
load_dotenv()

llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],model_id=DEFAULT_CONFIG["deep_think_llm"],max_tokens=16000)
quick_llm = get_model(provider=DEFAULT_CONFIG["llm_provider"],thinking=False, model_id=DEFAULT_CONFIG["quick_think_llm"],max_tokens=10000)

company_of_interest="AMZN"#"AMAZON"
trade_date="2025-08-19"

working_dir = DEFAULT_CONFIG['results_dir']
prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")
config = DEFAULT_CONFIG.copy()



# market trend
market_agent=create_market_analyst(quick_llm, False)

prompt=f"Analyze the market for {company_of_interest} for the trade date {trade_date}"

result=market_agent(prompt)
save_as_file(str(result), prefix, "market_report.txt") 




online=True
news_analyst_agent = create_news_analyst(quick_llm, online)
prompt=f"Analyze the news for {company_of_interest} for the trade date {trade_date}"
result=news_analyst_agent(prompt)
save_as_file(str(result), prefix, "news_report.txt") 

#memory_name = news_analyst_agent.state.get("memory_name")



bull_researcher=create_bull_researcher(llm, "bull_memory", config)
bear_researcher=create_bear_researcher(llm, "bear_memory", config)
research_manager = create_research_manager(llm, "invest_judge_memory", config)

research_debate = ConversationSwarm(
    agents=[
        bull_researcher,
        bear_researcher,
    ],
    summarizer_agent=research_manager,
    coordination="competitive"
)

market_report = read_file(working_dir,prefix,"market_report.txt")
news_report = read_file(working_dir,prefix,"news_report.txt")

investment_plan,messages = research_debate.run(
    f"Debate and decide on an investment plan for {company_of_interest} for the trade date {trade_date} based on the following reports:\n\n"
    f"Market Report:\n{market_report}\n\n"
    f"News Report:\n{news_report}"
)


# Saving history for relection
bull_history = "\n\n".join(messages[bull_researcher.name])
bear_history = "\n\n".join(messages[bear_researcher.name])
save_as_file(bull_history,working_dir,prefix,"bull_history.txt")
save_as_file(bear_history,working_dir,prefix,"bear_history.txt"
)
save_as_file(str(investment_plan),working_dir,prefix,"investment_plan.txt")



trader = create_trader(quick_llm, "trader_memory", config)
investment_plan = read_file(working_dir,prefix,"investment_plan.txt")
       
trader_decision = trader(
    f"Based on the following investment plan for {company_of_interest} for the trade date {trade_date}, what is your final trade decision?\n\n{investment_plan}"
)
# print(trader_decision)
save_as_file(str(trader_decision),working_dir,prefix,"trader_decision.txt")


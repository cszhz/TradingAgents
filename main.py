from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import os
load_dotenv()
# Create a custom config
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"  # Use a different model
config["backend_url"] = "https://ark.cn-beijing.volces.com/api/v3/"  # Use a different backend
# config["deep_think_llm"] = "doubao-seed-1-6-thinking-250615"  # Use a different model
config["deep_think_llm"] = "doubao-seed-1-6-250615"  # Use a different model
config["quick_think_llm"] = "doubao-seed-1-6-flash-250615"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Increase debate rounds
config["EXA_API_KEY"] = os.environ.get("EXA_API_KEY")
config["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

from tradingagents.dataflows.interface import get_stock_news_openai,get_fundamentals_openai

# print(get_stock_news_openai("month","2025-07-02"))
# print(get_fundamentals_openai("month","2025-07-02"))
# forward propagate
_, decision = ta.propagate("AMZN", "2025-07-02")
# print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns

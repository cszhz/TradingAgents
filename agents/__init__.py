"""
TradingAgents - Agent Modules

This package contains all the specialized trading agents used in the TradingAgents framework.
Each agent has a specific role in the trading analysis and decision-making process.

Available Agents:
- Market Analyst: Analyzes technical indicators and market trends
- News Analyst: Processes news and global events affecting markets
- Bull Researcher: Advocates for positive investment positions
- Bear Researcher: Advocates for cautious/negative investment positions
- Research Manager: Coordinates and summarizes research team debates
- Trader: Makes final trading decisions based on analysis
- ConversationSwarm: Manages multi-agent debates and discussions
"""

from .market_analyst import create_market_analyst
from .news_analyst import create_news_analyst
from .bull_researcher import create_bull_researcher
from .bear_researcher import create_bear_researcher
from .research_manager import create_research_manager
from .trader import create_trader
from .conversation_swarm import ConversationSwarm

__all__ = [
    "create_market_analyst",
    "create_news_analyst", 
    "create_bull_researcher",
    "create_bear_researcher",
    "create_research_manager",
    "create_trader",
    "ConversationSwarm"
]
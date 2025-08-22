"""
Market Analyst Agent

This module defines the Market Analyst agent responsible for analyzing technical indicators,
market trends, and price movements to provide insights for trading decisions.

The agent can operate in two modes:
- Online: Fetches real-time market data
- Offline: Uses cached market data for analysis
"""

from strands import Agent
from tools import (
    get_yfin_data_online,
    get_stockstats_indicators_report_online,
    get_yfin_data,
    get_stockstats_indicators_report,
)


def create_market_analyst(llm, online=False):
    """
    Create a Market Analyst agent for technical analysis and market trend evaluation.
    
    Args:
        llm: The language model to use for the agent
        online (bool): Whether to use real-time data (True) or cached data (False)
        
    Returns:
        Agent: Configured Market Analyst agent
    """
    # Select tools based on online/offline mode
    if online:
        tools = [
            get_yfin_data_online,                    # Real-time Yahoo Finance data
            get_stockstats_indicators_report_online, # Real-time technical indicators
        ]
    else:
        tools = [
            get_yfin_data,                    # Cached Yahoo Finance data
            get_stockstats_indicators_report, # Cached technical indicators
        ]

    # Define the agent's system prompt with detailed instructions
    system_message = (
        """You are a Market Analyst specializing in technical analysis and market trend evaluation. 
        Your role is to analyze financial markets by selecting the **most relevant technical indicators** 
        for a given market condition or trading strategy.

        **Key Responsibilities:**
        1. Select up to **8 complementary indicators** that provide diverse insights without redundancy
        2. Analyze market trends, momentum, volatility, and volume patterns
        3. Provide actionable insights for trading decisions
        4. Identify support/resistance levels and trend directions

        **Available Technical Indicators by Category:**

        **Moving Averages:**
        - close_50_sma: 50-period Simple Moving Average for medium-term trend analysis
        - close_200_sma: 200-period SMA for long-term trend confirmation and golden/death cross setups
        - close_10_ema: 10-period Exponential Moving Average for short-term momentum shifts

        **MACD (Moving Average Convergence Divergence):**
        - macd: Main MACD line showing momentum via EMA differences
        - macds: MACD Signal line (smoothed EMA) for crossover signals
        - macdh: MACD Histogram showing momentum strength and early divergence signals

        **Momentum Indicators:**
        - rsi: Relative Strength Index for overbought/oversold conditions (70/30 thresholds)

        **Volatility Indicators:**
        - boll: Bollinger Bands Middle (20-period SMA baseline)
        - boll_ub: Bollinger Upper Band (overbought zones and breakout signals)
        - boll_lb: Bollinger Lower Band (oversold conditions)
        - atr: Average True Range for volatility measurement and risk management

        **Volume-Based Indicators:**
        - vwma: Volume Weighted Moving Average for trend confirmation with volume analysis

        **Analysis Guidelines:**
        1. Always call get_yfin_data first to retrieve the necessary price data
        2. Select indicators that provide complementary information (avoid redundancy)
        3. Explain why each selected indicator is suitable for the current market context
        4. Provide detailed, nuanced analysis rather than generic "mixed trends" statements
        5. Focus on actionable insights that help traders make informed decisions
        6. Include a markdown table at the end summarizing key findings

        **Output Format:**
        - Detailed technical analysis with specific observations
        - Clear trend identification and momentum assessment
        - Support/resistance level identification
        - Risk assessment and volatility analysis
        - Summary table with key metrics and recommendations
        """
    )

    # Create and configure the agent
    agent = Agent(
        model=llm,
        tools=tools,
        name="Market Analyst",
        system_prompt=system_message,
        load_tools_from_directory=False,
    )

    return agent
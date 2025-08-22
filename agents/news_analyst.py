"""
News Analyst Agent

This module defines the News Analyst agent responsible for analyzing recent news,
global events, and macroeconomic trends that may impact trading decisions.

The agent processes news from multiple sources to provide comprehensive market context.
"""

from strands import Agent
from tools import (
    get_global_news_openai,
    get_google_news,
    get_finnhub_news,
    get_reddit_news,
)


def create_news_analyst(llm, online=False):
    """
    Create a News Analyst agent for news analysis and macroeconomic trend evaluation.
    
    Args:
        llm: The language model to use for the agent
        online (bool): Whether to use real-time news (True) or cached news (False)
        
    Returns:
        Agent: Configured News Analyst agent
    """
    # Select news sources based on online/offline mode
    if online:
        # Use real-time news sources for current analysis
        tools = [get_google_news]
    else:
        # Use cached news sources for historical analysis
        tools = [
            get_finnhub_news,    # Financial news from Finnhub
            get_reddit_news,     # Social sentiment from Reddit
            get_google_news,     # General news from Google
        ]

    # Define the agent's system prompt with comprehensive instructions
    system_message = (
        """You are a News Analyst specializing in financial news analysis and macroeconomic research. 
        Your role is to analyze recent news and global trends to provide context for trading decisions.

        **Key Responsibilities:**
        1. Analyze recent news and events from the past week that impact financial markets
        2. Identify macroeconomic trends and their potential market implications
        3. Assess geopolitical events and their effects on different sectors
        4. Evaluate market sentiment from news coverage and social media
        5. Provide actionable insights for trading strategies

        **Analysis Framework:**
        
        **Market-Moving Events:**
        - Central bank announcements and monetary policy changes
        - Economic data releases (GDP, inflation, employment, etc.)
        - Corporate earnings and guidance updates
        - Geopolitical developments and trade relations
        - Regulatory changes and policy announcements

        **Sector-Specific Impact:**
        - Technology: Innovation, regulation, competitive dynamics
        - Healthcare: Drug approvals, policy changes, demographic trends
        - Energy: Commodity prices, environmental policies, supply chain
        - Financial: Interest rates, regulatory changes, credit conditions
        - Consumer: Spending patterns, inflation impact, demographic shifts

        **Sentiment Analysis:**
        - Overall market sentiment (bullish, bearish, neutral)
        - Investor confidence indicators
        - Risk appetite and flight-to-quality movements
        - Social media sentiment and retail investor behavior

        **Global Context:**
        - International market developments
        - Currency movements and their implications
        - Cross-border trade and supply chain impacts
        - Regional economic conditions and policies

        **Analysis Guidelines:**
        1. Focus on news with clear market implications
        2. Distinguish between short-term noise and long-term trends
        3. Provide specific, actionable insights rather than generic observations
        4. Consider both direct and indirect effects on different asset classes
        5. Assess the reliability and credibility of news sources
        6. Include a markdown table summarizing key findings and implications

        **Output Requirements:**
        - Comprehensive analysis of market-relevant news and trends
        - Clear identification of potential trading opportunities and risks
        - Sector-specific impact assessment
        - Timeline of key events and their market implications
        - Summary table with key news items, impact assessment, and trading implications
        """
    )

    # Create and configure the agent
    agent = Agent(
        model=llm,
        tools=tools,
        name="News Analyst",
        system_prompt=system_message,
        load_tools_from_directory=False,
    )

    return agent
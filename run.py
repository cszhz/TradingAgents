#!/usr/bin/env python3
"""
TradingAgents Main Entry Point

This is the main entry point for the TradingAgents multi-agent trading framework.
It demonstrates how to use the framework to analyze a stock and make trading decisions.

Usage:
    python run.py

The script will:
1. Initialize market and news analysts
2. Run research team debate (bull vs bear researchers)
3. Generate trader decision based on analysis
4. Save all reports and decisions to the results directory
"""

import sys
import os
from pathlib import Path
from model_utils import get_model, save_as_file, read_file
from default_config import DEFAULT_CONFIG
import logging
from dotenv import load_dotenv

# Import agent creation functions
from agents import (
    create_market_analyst,
    create_news_analyst,
    create_research_manager,
    create_bear_researcher,
    create_bull_researcher,
    create_trader,
    ConversationSwarm,
)

# Load environment variables
load_dotenv()

def main():
    """Main function to run the trading analysis workflow."""
    
    # Initialize LLM models
    llm = get_model(
        provider=DEFAULT_CONFIG["llm_provider"],
        model_id=DEFAULT_CONFIG["deep_think_llm"],
        max_tokens=10000
    )
    quick_llm = get_model(
        provider=DEFAULT_CONFIG["llm_provider"],
        thinking=False,
        model_id=DEFAULT_CONFIG["quick_think_llm"],
        max_tokens=10000
    )

    # Configuration
    company_of_interest = "AMZN"  # Stock ticker to analyze
    trade_date = "2025-08-19"    # Analysis date
    
    working_dir = DEFAULT_CONFIG['results_dir']
    prefix = f"{company_of_interest}_{trade_date}".replace(" ", "_")
    config = DEFAULT_CONFIG.copy()

    print(f"Starting analysis for {company_of_interest} on {trade_date}")

    online = True
    '''
    # Step 1: Market Analysis
    print("Step 1: Running market analysis...")
    market_agent = create_market_analyst(quick_llm, online)
    prompt = f"Analyze the market for {company_of_interest} for the trade date {trade_date}"
    result = market_agent(prompt)
    save_as_file(str(result), working_dir,prefix, "market_report.txt")
    print("Market analysis completed.")

    # Step 2: News Analysis
    print("Step 2: Running news analysis...")
    news_analyst_agent = create_news_analyst(quick_llm, online)
    prompt = f"Analyze the news for {company_of_interest} for the trade date {trade_date}"
    result = news_analyst_agent(prompt)
    save_as_file(str(result), working_dir,prefix, "news_report.txt")
    print("News analysis completed.")
    '''
    # Step 3: Research Team Debate
    print("Step 3: Running research team debate...")
    bull_researcher = create_bull_researcher(llm, "bull_memory", config)
    bear_researcher = create_bear_researcher(llm, "bear_memory", config)
    research_manager = create_research_manager(llm, "invest_judge_memory", config)

    # Create debate swarm with competitive coordination
    research_debate = ConversationSwarm(
        agents=[bull_researcher, bear_researcher],
        summarizer_agent=research_manager,
        coordination="competitive"
    )

    # Load previous reports for context
    market_report = read_file(working_dir, prefix, "market_report.txt")
    news_report = read_file(working_dir, prefix, "news_report.txt")

    # Run the debate
    investment_plan, messages = research_debate.run(
        f"Debate and decide on an investment plan for {company_of_interest} "
        f"for the trade date {trade_date} based on the following reports:\n\n"
        f"Market Report:\n{market_report}\n\n"
        f"News Report:\n{news_report}"
    )

    # Save debate history and investment plan
    bull_history = "\n\n".join(messages[bull_researcher.name])
    bear_history = "\n\n".join(messages[bear_researcher.name])
    save_as_file(bull_history, working_dir, prefix, "bull_history.txt")
    save_as_file(bear_history, working_dir, prefix, "bear_history.txt")
    save_as_file(str(investment_plan), working_dir, prefix, "investment_plan.txt")
    print("Research team debate completed.")

    # Step 4: Trader Decision
    print("Step 4: Generating trader decision...")
    trader = create_trader(quick_llm, "trader_memory", config)
    investment_plan = read_file(working_dir, prefix, "investment_plan.txt")
    
    trader_decision = trader(
        f"Based on the following investment plan for {company_of_interest} "
        f"for the trade date {trade_date}, what is your final trade decision?\n\n"
        f"{investment_plan}"
    )
    
    save_as_file(str(trader_decision), working_dir, prefix, "trader_decision.txt")
    print("Trader decision completed.")

    print(f"\nAnalysis complete! Results saved to {working_dir}/{prefix}/")
    print("Generated files:")
    print("- market_report.txt")
    print("- news_report.txt") 
    print("- bull_history.txt")
    print("- bear_history.txt")
    print("- investment_plan.txt")
    print("- trader_decision.txt")

if __name__ == "__main__":
    main()
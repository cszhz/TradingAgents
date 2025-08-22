"""
TradingAgents Graph

This module implements the main TradingAgentsGraph class that orchestrates
the entire multi-agent trading workflow, from analysis to final decisions.
"""

import os
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from strands import Agent
from strands.telemetry import StrandsTelemetry

from agents import (
    create_market_analyst,
    create_news_analyst,
    create_research_manager,
    create_bear_researcher,
    create_bull_researcher,
    create_trader,
    ConversationSwarm,
)
from tools.memory import FinancialSituationMemory
from default_config import DEFAULT_CONFIG


class TradingAgentsGraph:
    """
    Main orchestrator for the TradingAgents multi-agent trading framework.
    
    This class coordinates the entire trading analysis workflow:
    1. Market and news analysis by specialist agents
    2. Research team debates between bull and bear analysts
    3. Trading decisions based on research recommendations
    4. Learning and reflection from past decisions
    """
    
    def __init__(self, llm, quick_llm=None, online=False, config=None):
        """
        Initialize the TradingAgentsGraph with models and configuration.
        
        Args:
            llm: Primary language model for complex reasoning tasks
            quick_llm: Fast language model for quick analysis tasks
            online (bool): Whether to use real-time data or cached data
            config (dict): Configuration overrides for default settings
        """
        # Setup configuration
        self.config = config if config else DEFAULT_CONFIG.copy()
        self.llm = llm
        self.quick_llm = quick_llm if quick_llm else llm
        self.online = online
        self.working_dir = self.config['results_dir']
        
        # Setup telemetry if configured
        self._setup_telemetry()
        
        # Create core analyst agents
        self.market_analyst = create_market_analyst(self.quick_llm, online)
        self.news_analyst = create_news_analyst(self.quick_llm, online)
        
        # Create research team agents
        self.research_manager = create_research_manager(llm, "invest_judge_memory", self.config)
        self.bear_researcher = create_bear_researcher(llm, "bear_memory", self.config)
        self.bull_researcher = create_bull_researcher(llm, "bull_memory", self.config)
        
        # Create trading agent
        self.trader = create_trader(self.quick_llm, "trader_memory", self.config)
        
        # Ensure working directory exists
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir, exist_ok=True)
    
    def _setup_telemetry(self):
        """Setup telemetry for tracking agent interactions if configured."""
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
        langfuse_endpoint = os.environ.get("LANGFUSE_HOST")
        
        if public_key and secret_key and langfuse_endpoint:
            print("Setting up telemetry tracking...")
            otel_endpoint = langfuse_endpoint + "/api/public/otel"
            auth_token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"
            
            strands_telemetry = StrandsTelemetry()
            strands_telemetry.setup_otlp_exporter()
    
    def save_as_file(self, text, prefix='', file_name=''):
        """
        Save text content to a file in the results directory.
        
        Args:
            text (str): Content to save
            prefix (str): Subdirectory prefix (usually ticker_date)
            file_name (str): Name of the file to save
        """
        full_dir = os.path.join(self.working_dir, prefix)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir, exist_ok=True)
        
        file_path = os.path.join(full_dir, file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(text)
    
    def read_file(self, prefix='', file_name=''):
        """
        Read text content from a file in the results directory.
        
        Args:
            prefix (str): Subdirectory prefix (usually ticker_date)
            file_name (str): Name of the file to read
            
        Returns:
            str: File content
        """
        file_path = os.path.join(self.working_dir, prefix, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"File not found: {file_path}")
    
    def gather_information_step(self, company_of_interest, trade_date):
        """
        Step 1: Gather information from market and news analysts.
        
        Args:
            company_of_interest (str): Stock ticker to analyze
            trade_date (str): Date for the analysis
            
        Returns:
            dict: Analysis results from all analysts
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ", "_")
        
        print(f"Gathering information for {company_of_interest} on {trade_date}...")
        
        # Define analysis tasks
        tasks = [
            (self.market_analyst, 
             f"Analyze the market for {company_of_interest} for the trade date {trade_date}", 
             "market_report.txt"),
            (self.news_analyst, 
             f"Analyze the news for {company_of_interest} for the trade date {trade_date}", 
             "news_report.txt")
        ]
        
        results = {}
        
        # Execute analysis tasks
        for analyst, prompt, filename in tasks:
            print(f"Running {analyst.name} analysis...")
            try:
                result = analyst(prompt)
                self.save_as_file(str(result), prefix, filename)
                results[filename] = str(result)
                print(f"{analyst.name} analysis completed")
            except Exception as e:
                print(f"Error in {analyst.name} analysis: {e}")
                results[filename] = f"Error: {e}"
        
        return results
    
    def research_debate_step(self, company_of_interest, trade_date, analysis_results):
        """
        Step 2: Conduct research team debate between bull and bear analysts.
        
        Args:
            company_of_interest (str): Stock ticker to analyze
            trade_date (str): Date for the analysis
            analysis_results (dict): Results from information gathering step
            
        Returns:
            tuple: (investment_plan, debate_messages)
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ", "_")
        
        print("Starting research team debate...")
        
        # Create debate swarm with competitive coordination
        research_debate = ConversationSwarm(
            agents=[self.bull_researcher, self.bear_researcher],
            summarizer_agent=self.research_manager,
            coordination="competitive"
        )
        
        # Prepare debate context with analysis results
        market_report = analysis_results.get("market_report.txt", "No market analysis available")
        news_report = analysis_results.get("news_report.txt", "No news analysis available")
        
        debate_prompt = (
            f"Debate and decide on an investment plan for {company_of_interest} "
            f"for the trade date {trade_date} based on the following reports:\n\n"
            f"Market Report:\n{market_report}\n\n"
            f"News Report:\n{news_report}"
        )
        
        # Run the debate
        investment_plan, messages = research_debate.run(debate_prompt)
        
        # Save debate results
        bull_history = "\n\n".join(messages.get(self.bull_researcher.name, []))
        bear_history = "\n\n".join(messages.get(self.bear_researcher.name, []))
        
        self.save_as_file(bull_history, prefix, "bull_history.txt")
        self.save_as_file(bear_history, prefix, "bear_history.txt")
        self.save_as_file(str(investment_plan), prefix, "investment_plan.txt")
        
        print("Research team debate completed")
        
        return investment_plan, messages
    
    def trading_decision_step(self, company_of_interest, trade_date):
        """
        Step 3: Make final trading decision based on research recommendations.
        
        Args:
            company_of_interest (str): Stock ticker to analyze
            trade_date (str): Date for the analysis
            
        Returns:
            str: Final trading decision
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ", "_")
        
        print("Making final trading decision...")
        
        # Load investment plan from research team
        try:
            investment_plan = self.read_file(prefix, "investment_plan.txt")
        except ValueError:
            investment_plan = "No investment plan available from research team"
        
        # Generate trading decision
        trader_prompt = (
            f"Based on the following investment plan for {company_of_interest} "
            f"for the trade date {trade_date}, what is your final trade decision?\n\n"
            f"{investment_plan}"
        )
        
        trader_decision = self.trader(trader_prompt)
        self.save_as_file(str(trader_decision), prefix, "trader_decision.txt")
        
        print("Trading decision completed")
        
        return str(trader_decision)
    
    def propagate(self, company_of_interest, trade_date):
        """
        Execute the complete trading analysis workflow.
        
        Args:
            company_of_interest (str): Stock ticker to analyze
            trade_date (str): Date for the analysis
            
        Returns:
            tuple: (final_state, final_decision) containing all results and final decision
        """
        print(f"Starting complete analysis for {company_of_interest} on {trade_date}")
        
        # Step 1: Information gathering
        analysis_results = self.gather_information_step(company_of_interest, trade_date)
        
        # Step 2: Research team debate
        investment_plan, debate_messages = self.research_debate_step(
            company_of_interest, trade_date, analysis_results
        )
        
        # Step 3: Trading decision
        final_decision = self.trading_decision_step(company_of_interest, trade_date)
        
        # Compile final state
        final_state = {
            "company": company_of_interest,
            "trade_date": trade_date,
            "analysis_results": analysis_results,
            "investment_plan": str(investment_plan),
            "debate_messages": debate_messages,
            "final_decision": final_decision
        }
        
        print(f"Complete analysis finished for {company_of_interest}")
        
        return final_state, final_decision
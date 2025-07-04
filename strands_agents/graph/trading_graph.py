from strands import Agent
from strands_agents.agents import (
    create_fundamentals_analyst,
    create_market_analyst,
    create_news_analyst,
    create_social_media_analyst,
    create_research_manager,
    create_risk_manager,
    create_bear_researcher,
    create_bull_researcher,
    create_risky_debator,
    create_safe_debator,
    create_neutral_debator,
    create_trader,
    ConversationSwarm,
    TradingReflector,
)
from strands_agents.tools.memory import FinancialSituationMemory
from strands_agents.default_config import DEFAULT_CONFIG
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


class TradingAgentsGraph:
    def __init__(self, llm, quick_llm=None, online=False,working_dir='./results'):
        self.config = DEFAULT_CONFIG.copy()
        self.llm = llm
        self.quick_llm = quick_llm
        self.online = online
        self.working_dir = working_dir
        # Create agents
        self.fundamentals_analyst = create_fundamentals_analyst(quick_llm, online)
        self.market_analyst = create_market_analyst(quick_llm, online)
        self.news_analyst = create_news_analyst(quick_llm, online)
        self.social_media_analyst = create_social_media_analyst(quick_llm, online)
        
        self.research_manager = create_research_manager(llm, "invest_judge_memory", self.config)
        self.risk_manager = create_risk_manager(llm, "risk_manager_memory", self.config)
        self.bear_researcher = create_bear_researcher(llm, "bear_memory", self.config)
        self.bull_researcher = create_bull_researcher(llm, "bull_memory", self.config)
        self.risky_debator = create_risky_debator(llm)
        self.safe_debator = create_safe_debator(llm)
        self.neutral_debator = create_neutral_debator(llm)
        
        self.trader = create_trader(quick_llm, "trader_memory", self.config)
        
        # Create reflector for learning from past decisions
        self.reflector = TradingReflector(llm, self.config)
        
        #check if folder exsit
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)


    def save_as_file(self,text,prefix='',file_name=''):
        if not os.path.exists(os.path.join(self.working_dir,prefix)):
            os.mkdir(os.path.join(self.working_dir,prefix))
        with open(os.path.join(self.working_dir,prefix,file_name), "w") as f:
            f.write(text)
            
    def read_file(self,prefix='',file_name=''):
        if os.path.exists(os.path.join(self.working_dir, prefix, file_name)):
            with open(os.path.join(self.working_dir,prefix, file_name), "r") as f:
                return f.read()
        else:
            raise ValueError(f"{os.path.join(self.working_dir,prefix, file_name)} not exist")

    def gather_information_step(self,company_of_interest, trade_date):
        """1. Analysts gather information
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")
        
        # Define analysis tasks
        tasks = [
            (self.fundamentals_analyst, f"Analyze the fundamentals of {company_of_interest} for the trade date {trade_date}", "fundamentals_report.txt"),
            (self.market_analyst, f"Analyze the market for {company_of_interest} for the trade date {trade_date}", "market_report.txt"),
            (self.news_analyst, f"Analyze the news for {company_of_interest} for the trade date {trade_date}", "news_report.txt"),
            (self.social_media_analyst, f"Analyze the social media sentiment for {company_of_interest} for the trade date {trade_date}", "social_media_report.txt")
        ]
        
        # Execute tasks in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_task = {executor.submit(analyst, prompt): (analyst, prompt, filename) for analyst, prompt, filename in tasks}
            
            for future in as_completed(future_to_task):
                analyst, prompt, filename = future_to_task[future]
                try:
                    result = future.result()
                    self.save_as_file(str(result), prefix, filename)
                except Exception as exc:
                    print(f'Analysis task generated an exception: {exc}')
        
        # Return the social media report (last one for compatibility)
        return self.read_file(prefix, "social_media_report.txt")
    
    def research_debate_step(self, company_of_interest, trade_date):
        """ 2. Research debate
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")
        research_debate = ConversationSwarm(
            agents=[
                self.bull_researcher,
                self.bear_researcher,
            ],
            summarizer_agent=self.research_manager,
            coordination="competitive"
        )
        
        fundamentals_report = self.read_file(prefix,"fundamentals_report.txt")
        market_report = self.read_file(prefix,"market_report.txt")
        news_report = self.read_file(prefix,"news_report.txt")
        social_media_report = self.read_file(prefix,"social_media_report.txt")

        investment_plan = research_debate.run(
            f"Debate and decide on an investment plan for {company_of_interest} based on the following reports:\n\n"
            f"Fundamentals Report:\n{fundamentals_report}\n\n"
            f"Market Report:\n{market_report}\n\n"
            f"News Report:\n{news_report}\n\n"
            f"Social Media Report:\n{social_media_report}"
        )
        print(investment_plan)
        self.save_as_file(str(investment_plan),prefix,"investment_plan.txt")
        return investment_plan
    
    def trader_decision_step(self, company_of_interest, trade_date):
        """3. Trader makes a decision
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")
        investment_plan = self.read_file(prefix,"investment_plan.txt")

       
        trader_decision = self.trader(
            f"Based on the following investment plan, what is your final trade decision?\n\n{investment_plan}"
        )
        print(trader_decision)
        self.save_as_file(str(trader_decision),prefix,"trader_decision.txt")
        return trader_decision
        
    def risk_debate_step(self,company_of_interest, trade_date):
        """4. Risk debate
        """
        prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")
        trader_decision = self.read_file(prefix,"trader_decision.txt")
        # self.trader_memory.add_situations([trader_decision])  # Add the trader's decision to the memory

        risk_debate = ConversationSwarm(
            agents=[
                self.risky_debator,
                self.safe_debator,
                self.neutral_debator,
            ],
            summarizer_agent=self.risk_manager,
            coordination="competitive"
        )
        final_decision = risk_debate.run(
            f"Debate the risk of the following trade decision and provide a final recommendation:\n\n{trader_decision}"
        )
        print(final_decision)
        self.save_as_file(str(final_decision),prefix,"final_decision.txt")
        return final_decision
    
    def reflection_step(self, company_of_interest, trade_date, returns_losses):
        """5. Reflection step - Learn from the trading decisions
        
        Args:
            company_of_interest: The stock symbol being traded
            trade_date: The date of the trade
            returns_losses: Performance results from the trading decisions
        """
        print("------------------# 5. Reflection and Learning----------------------------")
        prefix = f"{company_of_interest}_{trade_date}".replace(" ","_")

        # Build current state from saved reports
        current_state = {
            "market_report": self.read_file(prefix,"market_report.txt") ,
            "sentiment_report": self.read_file(prefix,"social_media_report.txt") ,
            "news_report": self.read_file(prefix,"news_report.txt") ,
            "fundamentals_report": self.read_file(prefix,"fundamentals_report.txt") ,
            "trader_investment_plan": self.read_file(prefix,"trader_decision.txt") ,
            "investment_debate_state": {
                "bull_history": self.read_file(prefix,"investment_plan.txt") ,
                "bear_history": self.read_file(prefix,"investment_plan.txt") ,
                "judge_decision": self.read_file(prefix,"investment_plan.txt")
            },
            "risk_debate_state": {
                "judge_decision": self.read_file(prefix,"final_decision.txt"),
            }
        }
        
        # Perform reflection on all components
        reflections = self.reflector.reflect_on_all_components(current_state, returns_losses)
        
        # Save reflections for future reference
        for component, reflection in reflections.items():
            self.save_as_file(str(reflection), prefix,f"reflection_{component}.txt")
            print(f"\n--- {component.upper()} REFLECTION ---")
            print(reflection)
        
        # Save a summary of all reflections
        reflection_summary = "\n\n".join([
            f"=== {component.upper()} REFLECTION ===\n{reflection}" 
            for component, reflection in reflections.items()
        ])
        self.save_as_file(reflection_summary,prefix, "reflection_summary.txt")
        
        return reflections
            
        
    def run(self, company_of_interest, trade_date, returns_losses=None):
        print("------------------# 1. Analysts gather information----------------------------")
        # self.gather_information_step(company_of_interest, trade_date)
        
        print("------------------# 2. Research debate----------------------------")
        self.research_debate_step(company_of_interest, trade_date)
        
        print("------------------# 3. Trader makes a decision----------------------------")
        # self.trader_decision_step(company_of_interest, trade_date)
        
        print("------------------# 4. Risk debate----------------------------")
        # final_decision = self.risk_debate_step(company_of_interest, trade_date)
        
        print (f"Job done, please find results")
        # return final_decision

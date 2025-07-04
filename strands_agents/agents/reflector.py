from strands import Agent, tool
from strands_agents.tools.memory import add_financial_situation_memories
from typing import Dict, Any, List, Tuple
from tradingagents.default_config import DEFAULT_CONFIG


def create_reflector(llm, config):
    """
    Create a reflector agent that analyzes trading decisions and learns from outcomes.
    
    Args:
        llm: The language model to use
        config: Configuration dictionary containing settings
    
    Returns:
        Agent: Configured reflector agent
    """
    system_message = """
You are an expert financial analyst tasked with reviewing trading decisions/analysis and providing a comprehensive, step-by-step analysis. 
Your goal is to deliver detailed insights into investment decisions and highlight opportunities for improvement, adhering strictly to the following guidelines:

1. Reasoning:
   - For each trading decision, determine whether it was correct or incorrect. A correct decision results in an increase in returns, while an incorrect decision does the opposite.
   - Analyze the contributing factors to each success or mistake. Consider:
     - Market intelligence.
     - Technical indicators.
     - Technical signals.
     - Price movement analysis.
     - Overall market data analysis 
     - News analysis.
     - Social media and sentiment analysis.
     - Fundamental data analysis.
     - Weight the importance of each factor in the decision-making process.

2. Improvement:
   - For any incorrect decisions, propose revisions to maximize returns.
   - Provide a detailed list of corrective actions or improvements, including specific recommendations (e.g., changing a decision from HOLD to BUY on a particular date).

3. Summary:
   - Summarize the lessons learned from the successes and mistakes.
   - Highlight how these lessons can be adapted for future trading scenarios and draw connections between similar situations to apply the knowledge gained.

4. Query:
   - Extract key insights from the summary into a concise sentence of no more than 1000 tokens.
   - Ensure the condensed sentence captures the essence of the lessons and reasoning for easy reference.

Adhere strictly to these instructions, and ensure your output is detailed, accurate, and actionable. You will also be given objective descriptions of the market from a price movements, technical indicator, news, and sentiment perspective to provide more context for your analysis.
"""
    agent = Agent(
        model=llm,
        name="trading_reflector",
        system_prompt=system_message,
    )
    
    agent.state.set("config", config)
    return agent


class TradingReflector:
    """
    Strands Agents implementation of the trading reflection system.
    Handles reflection on decisions and updating memory for different trading components.
    """

    def __init__(self, llm, config):
        """Initialize the reflector with a language model and configuration."""
        self.reflector_agent = create_reflector(llm, config)
        self.config = config

    def _extract_current_situation(self, current_state: Dict[str, Any]) -> str:
        """Extract the current market situation from the state."""
        situation_parts = []
        
        if "market_report" in current_state:
            situation_parts.append(f"MARKET REPORT:\n{current_state['market_report']}")
        
        if "sentiment_report" in current_state:
            situation_parts.append(f"SENTIMENT REPORT:\n{current_state['sentiment_report']}")
        
        if "news_report" in current_state:
            situation_parts.append(f"NEWS REPORT:\n{current_state['news_report']}")
        
        if "fundamentals_report" in current_state:
            situation_parts.append(f"FUNDAMENTALS REPORT:\n{current_state['fundamentals_report']}")

        return "\n\n".join(situation_parts)

    def _reflect_and_update_memory(
        self, 
        component_type: str, 
        decision_report: str, 
        situation: str, 
        returns_losses: str,
        memory_name: str
    ) -> str:
        """Generate reflection for a component and update its memory with error handling."""
        
        try:
            # Set the memory name for this reflection
            self.reflector_agent.state.set("memory_name", memory_name)
            self.reflector_agent.state.set("config", self.config)
            
            # Generate reflection using the reflector agent
            reflection_result = self.reflector_agent(
                f"Reflect on this {component_type} decision:\n\n"
                f"DECISION/ANALYSIS:\n{decision_report}\n\n"
                f"MARKET SITUATION:\n{situation}\n\n"
                f"PERFORMANCE RESULTS:\n{returns_losses}\n\n"
                f"Please provide a comprehensive reflection and analysis."
            )
            
            # Add the situation and reflection to memory with error handling
            try:
                situations_and_advice = [(situation, str(reflection_result))]
                add_financial_situation_memories(situations_and_advice, self.reflector_agent)
                print(f"✅ Successfully stored reflection for {component_type} in {memory_name}")
            except Exception as memory_error:
                print(f"⚠️  Failed to store reflection in memory for {component_type}: {memory_error}")
                # Continue without failing the entire reflection process
            
            return str(reflection_result)
            
        except Exception as e:
            print(f"❌ Error during reflection for {component_type}: {e}")
            # Return a basic reflection instead of failing completely
            return f"Reflection for {component_type}: Unable to generate detailed reflection due to error: {e}. Decision: {decision_report[:200]}..."

    def reflect_bull_researcher(self, current_state: Dict[str, Any], returns_losses: str) -> str:
        """Reflect on bull researcher's analysis and update memory."""
        situation = self._extract_current_situation(current_state)
        bull_debate_history = current_state.get("investment_debate_state", {}).get("bull_history", "")

        return self._reflect_and_update_memory(
            "BULL RESEARCHER", 
            bull_debate_history, 
            situation, 
            returns_losses,
            "bull_memory"
        )

    def reflect_bear_researcher(self, current_state: Dict[str, Any], returns_losses: str) -> str:
        """Reflect on bear researcher's analysis and update memory."""
        situation = self._extract_current_situation(current_state)
        bear_debate_history = current_state.get("investment_debate_state", {}).get("bear_history", "")

        return self._reflect_and_update_memory(
            "BEAR RESEARCHER", 
            bear_debate_history, 
            situation, 
            returns_losses,
            "bear_memory"
        )

    def reflect_trader(self, current_state: Dict[str, Any], returns_losses: str) -> str:
        """Reflect on trader's decision and update memory."""
        situation = self._extract_current_situation(current_state)
        trader_decision = current_state.get("trader_investment_plan", "")

        return self._reflect_and_update_memory(
            "TRADER", 
            trader_decision, 
            situation, 
            returns_losses,
            "trader_memory"
        )

    def reflect_invest_judge(self, current_state: Dict[str, Any], returns_losses: str) -> str:
        """Reflect on investment judge's decision and update memory."""
        situation = self._extract_current_situation(current_state)
        judge_decision = current_state.get("investment_debate_state", {}).get("judge_decision", "")

        return self._reflect_and_update_memory(
            "INVESTMENT JUDGE", 
            judge_decision, 
            situation, 
            returns_losses,
            "invest_judge_memory"
        )

    def reflect_risk_manager(self, current_state: Dict[str, Any], returns_losses: str) -> str:
        """Reflect on risk manager's decision and update memory."""
        situation = self._extract_current_situation(current_state)
        risk_judge_decision = current_state.get("risk_debate_state", {}).get("judge_decision", "")

        return self._reflect_and_update_memory(
            "RISK MANAGER", 
            risk_judge_decision, 
            situation, 
            returns_losses,
            "risk_manager_memory"
        )

    def reflect_on_all_components(
        self, 
        current_state: Dict[str, Any], 
        returns_losses: str
    ) -> Dict[str, str]:
        """
        Reflect on all trading components and return a summary of reflections with error handling.
        
        Args:
            current_state: Current trading state with all component decisions
            returns_losses: Performance results from the trading decisions
            
        Returns:
            Dict[str, str]: Dictionary mapping component names to their reflections
        """
        reflections = {}
        
        # Define reflection methods and their names
        reflection_methods = [
            ("bull_researcher", self.reflect_bull_researcher),
            ("bear_researcher", self.reflect_bear_researcher),
            ("trader", self.reflect_trader),
            ("invest_judge", self.reflect_invest_judge),
            ("risk_manager", self.reflect_risk_manager),
        ]
        
        # Reflect on each component with individual error handling
        for component_name, reflection_method in reflection_methods:
            try:
                print(f"Generating reflection for {component_name}...")
                reflection = reflection_method(current_state, returns_losses)
                reflections[component_name] = reflection
                print(f"✅ Successfully generated reflection for {component_name}")
            except Exception as e:
                error_msg = f"Failed to generate reflection for {component_name}: {e}"
                print(f"❌ {error_msg}")
                reflections[component_name] = f"Error: {error_msg}"
                # Continue with other components instead of failing completely
        
        print(f"Completed reflection generation for {len(reflections)} components")
        return reflections

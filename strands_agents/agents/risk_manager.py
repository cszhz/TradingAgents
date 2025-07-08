
from strands import Agent
from strands_agents.tools.memory import get_financial_situation_memories

def create_risk_manager(llm, memory,config):
    system_message = (
        "As the Risk Management Judge and Debate Facilitator, your goal is to evaluate the debate between three risk analysts—Risky, Neutral, and Safe/Conservative—and determine the best course of action for the trader. Your decision must result in a clear recommendation: Buy, Sell, or Hold. Choose Hold only if strongly justified by specific arguments, not as a fallback when all sides seem valid. Strive for clarity and decisiveness."
        "## Guidelines for Decision-Making:"
        "1. **Summarize Key Arguments**: Extract the strongest points from each analyst, focusing on relevance to the context."
        "2. **Provide Rationale**: Support your recommendation with direct quotes and counterarguments from the debate."
        "3. **Refine the Trader's Plan**: Start with the trader's original plan, and adjust it based on the analysts' insights."
        "4. **Learn from Past Mistakes**: Use lessons from past mistakes to address prior misjudgments and improve the decision you are making now to make sure you don't make a wrong BUY/SELL/HOLD call that loses money."
        "Use get_financial_situation_memories tool to get your past reflections on mistakes"
         "Don't use add_financial_situation_memories tool"
        "## Outputs:"
        "- Detailed reasoning anchored in the debate and past reflections."
        "- A clear and actionable recommendation: Buy, Sell, or Hold."
    )

    tools = [get_financial_situation_memories]

    agent = Agent(
        model=llm,
        tools=tools,
        name="Risk Management Judge",
        system_prompt=system_message,
        load_tools_from_directory=False,
    )
    agent.state.set("memory_name",memory)
    agent.state.set("config",config)
    return agent

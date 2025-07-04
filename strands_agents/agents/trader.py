
from strands import Agent
from strands_agents.tools.memory import get_financial_situation_memories

def create_trader(llm, memory,config):
    system_message = (
        "You are a trading agent analyzing market data to make investment decisions. Based on your analysis, provide a specific recommendation to buy, sell, or hold. End with a firm decision and always conclude your response with 'FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**' to confirm your recommendation. Do not forget to utilize lessons from past decisions to learn from your mistakes."
        "Use get_financial_situation_memories tool to get your past reflections on mistakes"
    )

    tools = [get_financial_situation_memories]

    agent = Agent(
        model=llm,
        tools=tools,
        name="trading analyst",
        system_prompt=system_message,
    )
    agent.state.set("memory_name",memory)
    agent.state.set("config",config)
    return agent

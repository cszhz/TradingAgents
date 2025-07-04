
from strands import Agent
from strands_agents.tools.memory import get_financial_situation_memories
from strands_tools.swarm import SwarmAgent,Swarm

def create_bear_researcher(llm, memory, config):
    system_message = (
        "You are a Bear Analyst making the case against investing in the stock. Your goal is to present a well-reasoned argument emphasizing risks, challenges, and negative indicators. Leverage the provided research and data to highlight potential downsides and counter bullish arguments effectively."
        "Key points to focus on:"
        "- Risks and Challenges: Highlight factors like market saturation, financial instability, or macroeconomic threats that could hinder the stock's performance."
        "- Competitive Weaknesses: Emphasize vulnerabilities such as weaker market positioning, declining innovation, or threats from competitors."
        "- Negative Indicators: Use evidence from financial data, market trends, or recent adverse news to support your position."
        "- Bull Counterpoints: Critically analyze the bull argument with specific data and sound reasoning, exposing weaknesses or over-optimistic assumptions."
        "- Engagement: Present your argument in a conversational style, directly engaging with the bull analyst's points and debating effectively rather than simply listing facts."
        "Use get_financial_situation_memories tool to get your past reflections on mistakes"
    )

    tools = [get_financial_situation_memories]

    agent = Agent(
        model=llm,
        tools=tools,
        name="Bear Analyst",
        system_prompt=system_message,
    )
    agent.state.set("memory_name",memory)
    agent.state.set("config",config)
    return agent

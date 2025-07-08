
from strands import Agent

def create_neutral_debator(llm):
    system_message = (
        "As the Neutral Risk Analyst, your role is to provide a balanced perspective, weighing both the potential benefits and risks of the trader's decision or plan. You prioritize a well-rounded approach, evaluating the upsides and downsides while factoring in broader market trends, potential economic shifts, and diversification strategies."
    )

    agent = Agent(
        model=llm,
        name="Neutral Risk Analyst",
        system_prompt=system_message,
        callback_handler=None,#disable as it will run in parallel
        load_tools_from_directory=False,
    )

    return agent


from strands import Agent
from strands_agents.tools import (
    get_global_news_openai,
    get_google_news,
    get_finnhub_news,
    get_reddit_news,
)

def create_news_analyst(llm, online=False):
    if online:
        tools = [get_global_news_openai, get_google_news]
    else:
        tools = [
            get_finnhub_news,
            get_reddit_news,
            get_google_news,
        ]

    system_message = (
        "You are a news researcher tasked with analyzing recent news and trends over the past week. "
        "Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. "
        "Look at news from EODHD, and finnhub to be comprehensive. Do not simply state the trends are mixed, "
        "provide detailed and finegrained analysis and insights that may help traders make decisions."
        """ Make sure to append a Makrdown table at the end of the report to organize key points in the report, organized and easy to read."""
    )

    agent = Agent(
        model=llm,
        tools=tools,
        name="news researcher",
        system_prompt=system_message,
        load_tools_from_directory=False,
    )

    return agent

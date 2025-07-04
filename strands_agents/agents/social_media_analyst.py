
from strands import Agent
from strands_agents.tools import (
    get_stock_news_openai,
    get_reddit_stock_info,
)

def create_social_media_analyst(llm, online=False):
    if online:
        tools = [get_stock_news_openai]
    else:
        tools = [
            get_reddit_stock_info,
        ]

    system_message = (
        "You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, "
        "recent company news, and public sentiment for a specific company over the past week. You will be given a company's name "
        "your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors "
        "on this company's current state after looking at social media and what people are saying about that company, "
        "analyzing sentiment data of what people feel each day about the company, and looking at recent company news. "
        "Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, "
        "provide detailed and finegrained analysis and insights that may help traders make decisions."
        """ Make sure to append a Makrdown table at the end of the report to organize key points in the report, organized and easy to read."""
    )

    agent = Agent(
        model=llm,
        tools=tools,
        name="social media analyst",
        system_prompt=system_message,
    )

    return agent

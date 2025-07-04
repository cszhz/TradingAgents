
from strands import Agent
from strands_agents.tools import (
    get_fundamentals_openai,
    get_finnhub_company_insider_sentiment,
    get_finnhub_company_insider_transactions,
    get_simfin_balance_sheet,
    get_simfin_cashflow,
    get_simfin_income_stmt,
)

def create_fundamentals_analyst(llm, online=False):    
    if online:
        tools = [get_fundamentals_openai]
    else:
        tools = [
            get_finnhub_company_insider_sentiment,
            get_finnhub_company_insider_transactions,
            get_simfin_balance_sheet,
            get_simfin_cashflow,
            get_simfin_income_stmt,
        ]

    system_message = (
        "You are a researcher tasked with analyzing fundamental information over the past week about a company. "
        "Please write a comprehensive report of the company's fundamental information such as financial documents, "
        "company profile, basic company financials, company financial history, insider sentiment and insider transactions "
        "to gain a full view of the company's fundamental information to inform traders. Make sure to include as much detail as possible. "
        "Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
        " Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."
    )

    agent = Agent(
        model=llm,
        tools=tools,
        name="fundamental researcher",
        system_prompt=system_message,
    )

    return agent

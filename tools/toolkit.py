
from strands import tool
from typing import Annotated
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os
import yfinance as yf
from openai import OpenAI

from dataflows.interface import (
    get_finnhub_news as get_finnhub_news_orig,
    get_finnhub_company_insider_sentiment as get_finnhub_company_insider_sentiment_orig,
    get_finnhub_company_insider_transactions as get_finnhub_company_insider_transactions_orig,
    get_google_news as get_google_news_orig,
    get_reddit_global_news as get_reddit_global_news_orig,
    get_reddit_company_news as get_reddit_company_news_orig,
    get_simfin_balance_sheet as get_simfin_balance_sheet_orig,
    get_simfin_cashflow as get_simfin_cashflow_orig,
    get_simfin_income_statements as get_simfin_income_statements_orig,
    get_stock_stats_indicators_window as get_stock_stats_indicators_window_orig,
    get_YFin_data as get_YFin_data_orig,
    get_YFin_data_online as get_YFin_data_online_orig,
    get_stock_news_openai as get_stock_news_openai_orig,
    get_global_news_openai as get_global_news_openai_orig,
    get_fundamentals_openai as get_fundamentals_openai_orig,
)
from default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG

@tool
def get_reddit_news(
    curr_date: Annotated[str, "Date you want to get news for in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve global news from Reddit within a specified time frame.
    Args:
        curr_date (str): Date you want to get news for in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the latest global news from Reddit in the specified time frame.
    """
    
    return get_reddit_global_news_orig(curr_date, 7, 5)

@tool
def get_finnhub_news(
    ticker: Annotated[
        str,
        "Search query of a company, e.g. 'AAPL, TSM, etc.",
    ],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    """
    Retrieve the latest news about a given stock from Finnhub within a date range
    Args:
        ticker (str): Ticker of a company. e.g. AAPL, TSM
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing news about the company within the date range from start_date to end_date
    """

    end_date_str = end_date

    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    look_back_days = (end_date - start_date).days

    return get_finnhub_news_orig(
        ticker, end_date_str, look_back_days
    )

@tool
def get_reddit_stock_info(
    ticker: Annotated[
        str,
        "Ticker of a company. e.g. AAPL, TSM",
    ],
    curr_date: Annotated[str, "Current date you want to get news for"],
) -> str:
    """
    Retrieve the latest news about a given stock from Reddit, given the current date.
    Args:
        ticker (str): Ticker of a company. e.g. AAPL, TSM
        curr_date (str): current date in yyyy-mm-dd format to get news for
    Returns:
        str: A formatted dataframe containing the latest news about the company on the given date
    """

    return get_reddit_company_news_orig(ticker, curr_date, 7, 5)

@tool
def get_yfin_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
    """

    return get_YFin_data_orig(symbol, start_date, end_date)

@tool
def get_yfin_data_online(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
    """

    return get_YFin_data_online_orig(symbol, start_date, end_date)

@tool
def get_stockstats_indicators_report(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[
        str, "technical indicator to get the analysis and report of"
    ],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"] = 30,
) -> str:
    """
    Retrieve stock stats indicators for a given ticker symbol and indicator.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        indicator (str): Technical indicator to get the analysis and report of
        curr_date (str): The current trading date you are trading on, YYYY-mm-dd
        look_back_days (int): How many days to look back, default is 30
    Returns:
        str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
    """

    return get_stock_stats_indicators_window_orig(
        symbol, indicator, curr_date, look_back_days, False
    )

@tool
def get_stockstats_indicators_report_online(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[
        str, "technical indicator to get the analysis and report of"
    ],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"] = 30,
) -> str:
    """
    Retrieve stock stats indicators for a given ticker symbol and indicator.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        indicator (str): Technical indicator to get the analysis and report of
        curr_date (str): The current trading date you are trading on, YYYY-mm-dd
        look_back_days (int): How many days to look back, default is 30
    Returns:
        str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
    """

    return get_stock_stats_indicators_window_orig(
        symbol, indicator, curr_date, look_back_days, True
    )

@tool
def get_finnhub_company_insider_sentiment(
    ticker: Annotated[str, "ticker symbol for the company"],
    curr_date: Annotated[
        str,
        "current date of you are trading at, yyyy-mm-dd",
    ],
):
    """
    Retrieve insider sentiment information about a company (retrieved from public SEC information) for the past 30 days
    Args:
        ticker (str): ticker symbol of the company
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
        str: a report of the sentiment in the past 30 days starting at curr_date
    """

    return get_finnhub_company_insider_sentiment_orig(
        ticker, curr_date, 30
    )

@tool
def get_finnhub_company_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[
        str,
        "current date you are trading at, yyyy-mm-dd",
    ],
):
    """
    Retrieve insider transaction information about a company (retrieved from public SEC information) for the past 30 days
    Args:
        ticker (str): ticker symbol of the company
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
        str: a report of the company's insider transactions/trading information in the past 30 days
    """

    return get_finnhub_company_insider_transactions_orig(
        ticker, curr_date, 30
    )

@tool
def get_simfin_balance_sheet(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual/quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    """
    Retrieve the most recent balance sheet of a company
    Args:
        ticker (str): ticker symbol of the company
        freq (str): reporting frequency of the company's financial history: annual / quarterly
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
        str: a report of the company's most recent balance sheet
    """

    return get_simfin_balance_sheet_orig(ticker, freq, curr_date)

@tool
def get_simfin_cashflow(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual/quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    """
    Retrieve the most recent cash flow statement of a company
    Args:
        ticker (str): ticker symbol of the company
        freq (str): reporting frequency of the company's financial history: annual / quarterly
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
            str: a report of the company's most recent cash flow statement
    """

    return get_simfin_cashflow_orig(ticker, freq, curr_date)

@tool
def get_simfin_income_stmt(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[
        str,
        "reporting frequency of the company's financial history: annual/quarterly",
    ],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
):
    """
    Retrieve the most recent income statement of a company
    Args:
        ticker (str): ticker symbol of the company
        freq (str): reporting frequency of the company's financial history: annual / quarterly
        curr_date (str): current date you are trading at, yyyy-mm-dd
    Returns:
            str: a report of the company's most recent income statement
    """

    return get_simfin_income_statements_orig(
        ticker, freq, curr_date
    )

@tool
def get_google_news(
    query: Annotated[str, "Query to search with"],
    curr_date: Annotated[str, "Curr date in yyyy-mm-dd format"],
):
    """
    Retrieve the latest news from Google News based on a query and date range.
    Args:
        query (str): Query to search with
        curr_date (str): Current date in yyyy-mm-dd format
        look_back_days (int): How many days to look back
    Returns:
        str: A formatted string containing the latest news from Google News based on the query and date range.
    """

    return get_google_news_orig(query, curr_date, 7)

@tool
def get_stock_news_openai(
    ticker: Annotated[str, "the company's ticker"],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
):
    """
    Retrieve the latest news about a given stock by using OpenAI's news API.
    Args:
        ticker (str): Ticker of a company. e.g. AAPL, TSM
        curr_date (str): Current date in yyyy-mm-dd format
    Returns:
        str: A formatted string containing the latest news about the company on the given date.
    """

    return get_stock_news_openai_orig(ticker, curr_date)

@tool
def get_global_news_openai(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
):
    """
    Retrieve the latest macroeconomics news on a given date using OpenAI's macroeconomics news API.
    Args:
        curr_date (str): Current date in yyyy-mm-dd format
    Returns:
        str: A formatted string containing the latest macroeconomic news on the given date.
    """

    return get_global_news_openai_orig(curr_date)

@tool
def get_fundamentals_openai(
    ticker: Annotated[str, "the company's ticker"],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
):
    """
    Retrieve the latest fundamental information about a given stock on a given date by using OpenAI's news API.
    Args:
        ticker (str): Ticker of a company. e.g. AAPL, TSM
        curr_date (str): Current date in yyyy-mm-dd format
    Returns:
        str: A formatted string containing the latest fundamental information about the company on the given date.
    """

    return get_fundamentals_openai_orig(
        ticker, curr_date
    )

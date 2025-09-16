
from strands import tool
from typing import Annotated

from dataflows.interface import (
    get_google_news as get_google_news_orig,
    get_stock_stats_indicators_window as get_stock_stats_indicators_window_orig,
    get_YFin_data as get_YFin_data_orig,
    get_YFin_data_online as get_YFin_data_online_orig,
)
from default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG

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

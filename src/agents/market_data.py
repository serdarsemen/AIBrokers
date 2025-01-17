from langchain_openai.chat_models import ChatOpenAI

from agents.state import AgentState
from tools.api import get_price_API_HYPERLIQUID, get_LS_OI_Copin

from datetime import datetime


def check_data_valid(crypto, start_date, end_date):
    # Set default dates
    end_date = end_date or datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        # Calculate 1 months before end_date
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (
            end_date_obj.replace(month=end_date_obj.month - 1)
            if end_date_obj.month > 1
            else end_date_obj.replace(
                year=end_date_obj.year - 1, month=end_date_obj.month + 11
            )
        )
        start_date = start_date.strftime("%Y-%m-%d")
    else:
        start_date = start_date

    prices = get_price_API_HYPERLIQUID(
        pair=crypto,
        open_time=start_date,
        close_time=end_date,
    )
    insider_trades = get_LS_OI_Copin(pair=crypto)
    if isinstance(prices, str) | isinstance(insider_trades, str):
        print("Data invalid")
        return False
    else:
        return True


def market_data_agent(state: AgentState):
    """Responsible for gathering and preprocessing market data"""
    messages = state["messages"]
    data = state["data"]
    # Set default dates
    end_date = data["end_date"] or datetime.now().strftime("%Y-%m-%d")
    if not data["start_date"]:
        # Calculate 1 months before end_date
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (
            end_date_obj.replace(month=end_date_obj.month - 1)
            if end_date_obj.month > 1
            else end_date_obj.replace(
                year=end_date_obj.year - 1, month=end_date_obj.month + 11
            )
        )
        start_date = start_date.strftime("%Y-%m-%d")
    else:
        start_date = data["start_date"]

    # Get the historical price data

    prices = get_price_API_HYPERLIQUID(
        pair=data["crypto"],
        open_time=start_date,
        close_time=end_date,
    )

    # Get the insider trades
    insider_trades = get_LS_OI_Copin(pair=data["crypto"])

    return {
        "messages": messages,
        "data": {
            **data,
            "prices": prices,
            "start_date": start_date,
            "end_date": end_date,
            "insider_trades": insider_trades,
        },
    }

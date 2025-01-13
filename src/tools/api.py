import os
from typing import Dict, Any, List
import pandas as pd
import requests
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


load_dotenv(".env", override=True)

HYPERLIQUID_API_URL = os.environ.get("HYPERLIQUID_API_URL")
BINANCE_API_URL = os.environ.get("BINANCE_API_URL")
COPIN_POSITIONS_API_URL = os.environ.get("COPIN_POSITIONS_API_URL")

USERNAME_ELS = os.environ.get("USERNAME_ELS")
PASSWORD_ELS = os.environ.get("PASSWORD_ELS")


# def get_financial_metrics(
#     ticker: str,
#     report_period: str,
#     period: str = 'ttm',
#     limit: int = 1
# ) -> List[Dict[str, Any]]:
#     """Fetch financial metrics from the API."""
#     headers = {"X-API-KEY": FINANCIAL_DATASETS_API_KEY}
#     url = (
#         f"https://api.financialdatasets.ai/financial-metrics/"
#         f"?ticker={ticker}"
#         f"&report_period_lte={report_period}"
#         f"&limit={limit}"
#         f"&period={period}"
#     )
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(
#             f"Error fetching data: {response.status_code} - {response.text}"
#         )
#     data = response.json()
#     financial_metrics = data.get("financial_metrics")
#     if not financial_metrics:
#         raise ValueError("No financial metrics returned")
#     return financial_metrics

# def search_line_items(
#     ticker: str,
#     line_items: List[str],
#     period: str = 'ttm',
#     limit: int = 1
# ) -> List[Dict[str, Any]]:
#     """Fetch cash flow statements from the API."""
#     headers = {"X-API-KEY": FINANCIAL_DATASETS_API_KEY}
#     url = "https://api.financialdatasets.ai/financials/search/line-items"

#     body = {
#         "tickers": [ticker],
#         "line_items": line_items,
#         "period": period,
#         "limit": limit
#     }
#     response = requests.post(url, headers=headers, json=body)
#     if response.status_code != 200:
#         raise Exception(
#             f"Error fetching data: {response.status_code} - {response.text}"
#         )
#     data = response.json()
#     search_results = data.get("search_results")
#     if not search_results:
#         raise ValueError("No search results returned")
#     return search_results

# def get_insider_trades(
#     ticker: str,
#     end_date: str,
#     limit: int = 5,
# ) -> List[Dict[str, Any]]:
#     """
#     Fetch insider trades for a given ticker and date range.
#     """
#     headers = {"X-API-KEY": FINANCIAL_DATASETS_API_KEY}
#     url = (
#         f"https://api.financialdatasets.ai/insider-trades/"
#         f"?ticker={ticker}"
#         f"&filing_date_lte={end_date}"
#         f"&limit={limit}"
#     )
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(
#             f"Error fetching data: {response.status_code} - {response.text}"
#         )
#     data = response.json()
#     insider_trades = data.get("insider_trades")
#     if not insider_trades:
#         raise ValueError("No insider trades returned")
#     return insider_trades

# def get_market_cap(
#     ticker: str,
# ) -> List[Dict[str, Any]]:
#     """Fetch market cap from the API."""
#     headers = {"X-API-KEY": FINANCIAL_DATASETS_API_KEY}
#     url = (
#         f'https://api.financialdatasets.ai/company/facts'
#         f'?ticker={ticker}'
#     )

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(
#             f"Error fetching data: {response.status_code} - {response.text}"
#         )
#     data = response.json()
#     company_facts = data.get('company_facts')
#     if not company_facts:
#         raise ValueError("No company facts returned")
#     return company_facts.get('market_cap')

# def get_prices(
#     ticker: str,
#     start_date: str,
#     end_date: str
# ) -> List[Dict[str, Any]]:
#     """Fetch price data from the API."""
#     url = (
#         f"https://api.financialdatasets.ai/prices/"
#         f"?ticker={ticker}"
#         f"&interval=day"
#         f"&interval_multiplier=1"
#         f"&start_date={start_date}"
#         f"&end_date={end_date}"
#     )
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(
#             f"Error fetching data: {response.status_code} - {response.text}"
#         )
#     data = response.json()
#     prices = data.get("prices")
#     if not prices:
#         raise ValueError("No price data returned")
#     return prices


def date_to_timestamp(date):
    if (isinstance(date,str)):
        date = datetime.strptime(date, '%Y-%m-%d')
    timestamp_seconds = datetime.timestamp(date)
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    return timestamp_milliseconds


def connect_price_API_HYPERLIQUID(pair, open_time, close_time):
    open_time = date_to_timestamp(open_time)
    close_time = date_to_timestamp(close_time)
    APIURL = HYPERLIQUID_API_URL
    # pair_mapping = {
    #     "RND-USDT": "RENDER",
    #     "PEPE-USDT": "kPEPE",
    #     "BONK-USDT": "kBONK",
    #     "SHIB-USDT": "kSHIB",
    #     "FLOKI-USDT": "kFLOKI",
    #     "DOGS-USDT": "kFLOKI",
    #     # Thêm các cặp khác nếu cần
    # }
    # pair = pair.replace("-USDT", "")
    # pair = pair.replace("1000", "k")

    # pair = pair_mapping.get(pair, pair)


    # Body dữ liệu
    data = {
        "type": "candleSnapshot",
        "req": {
            "coin": pair,
            "interval": "1D",
            "startTime": open_time,
            "endTime": close_time,
        },
    }

    # Header cho request (nếu cần thiết)
    headers = {"Content-Type": "application/json"}

    # Gửi POST request

    response = requests.post(APIURL, json=data, headers=headers)
    data = response.json()
    df = pd.DataFrame(data)
    df.rename(
        columns={
            "t": "timestamp",
            "T": "close_time",
            "s": "symbol",
            "i": "interval",
            "o": "open",
            "c": "close",
            "h": "high",
            "l": "low",
            "v": "volume",
            "n": "number_of_trades",
        },
        inplace=True,
    )

    df = df[["open", "close", "high", "low","volume"]]
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)

    
    return df


def get_price_API_BINANCE(pair, open_time, close_time, limit: int = 1000):
    """Lấy dữ liệu từ API"""
    open_time = date_to_timestamp(open_time)
    close_time = date_to_timestamp(close_time)
    APIURL = BINANCE_API_URL+"/fapi/v1/continuousKlines"
    # pair_mapping = {
    #     "SHIBUSDT": "1000SHIBUSDT",
    #     "PEPEUSDT": "1000PEPEUSDT",
    #     "BONKUSDT": "1000BONKUSDT",
    #     "RNDRUSDT": "RENDERUSDT",
    #     # Thêm các cặp khác nếu cần
    # }
    # pair = pair.replace("-", "")
    # pair = pair_mapping.get(pair, pair)
    pair = pair +"USDT"
    paramsMap = {
        "pair": pair,
        "contractType": "PERPETUAL",
        "interval": "1h",
        "startTime": open_time,
        "endTime": close_time,
        "limit": limit,
    }

    # Gửi yêu cầu GET với paramsMap
    response = requests.get(APIURL, params=paramsMap)
    data = response.json()
    df = pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    
    df = df[["open", "close", "high", "low","volume"]]
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    

    return df

def get_LSRatio_Binance(pair):
    APIURL = BINANCE_API_URL+"/futures/data/topLongShortPositionRatio"
    pair = pair +"USDT"
    paramsMap = {
        "symbol": pair,
        "period": "1d",
        "limit" :1

    }
    response = requests.get(APIURL, params=paramsMap)
    data = response.json()
    df = pd.DataFrame(data)
    LSRatio = df["longShortRatio"][0]
    
    return float(LSRatio)

def get_OI_position_Copin(pair:str, isLong:bool):
    APIURL = COPIN_POSITIONS_API_URL
    pair = pair+"-USDT"
    if(isLong):
        value_long = "true"
    else:
        value_long = "false"
    query = {
    "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "isLong": {
                                "value": value_long
                            }
                        }
                    },
                    {
                        "term": {
                            "status": {
                                "value": "OPEN"
                            }
                        }
                    },
                    {
                        "term":{
                            "pair": {
                                "value": pair
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "total_size": {
                "sum": {
                    "field": "size"
                }
            }
        }
        
    }
    
    username = USERNAME_ELS
    password = PASSWORD_ELS
    response = requests.post(APIURL, auth=HTTPBasicAuth(username, password), json=query)
    data = response.json()
    total_size = data["aggregations"]["total_size"]["value"]
    return total_size

def get_LS_OI_Copin(pair):
    
    longOI = get_OI_position_Copin(pair,True)
    shortOI = get_OI_position_Copin(pair,False)
    
    
    
    return longOI, shortOI
    
    



# def prices_to_df(prices: List[Dict[str, Any]]) -> pd.DataFrame:
#     """Convert prices to a DataFrame."""
#     df = pd.DataFrame(prices)
#     df["Date"] = pd.to_datetime(df["time"])
#     df.set_index("Date", inplace=True)
#     numeric_cols = ["open", "close", "high", "low", "volume"]
#     for col in numeric_cols:
#         df[col] = pd.to_numeric(df[col], errors="coerce")
#     df.sort_index(inplace=True)
#     return df

# # Update the get_price_data function to use the new functions
# def get_price_data(
#     ticker: str,
#     start_date: str,
#     end_date: str
# ) -> pd.DataFrame:
#     prices = get_prices(ticker, start_date, end_date)
#     return prices_to_df(prices)



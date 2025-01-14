import math

from langchain_core.messages import HumanMessage

from agents.state import AgentState, show_agent_reasoning

import json
import ast

##### Risk Management Agent #####
def risk_management_agent(state: AgentState):
    """Evaluates portfolio risk and sets position limits based on comprehensive risk analysis."""
    show_reasoning = state["metadata"]["show_reasoning"]
    portfolio = state["data"]["portfolio"]
    cash = portfolio['cash']
    data = state["data"]
    max_loss = 0.05 #Loss maximum for the fund
    prices_df = data["prices"]

    # Fetch messages from other agents
    technical_message = next(msg for msg in state["messages"] if msg.name == "technical_analyst_agent")
    sentiment_message = next(msg for msg in state["messages"] if msg.name == "sentiment_agent")
    try:
        technical_signals = json.loads(technical_message.content)
        sentiment_signals = json.loads(sentiment_message.content)
    except Exception as e:
        technical_signals = ast.literal_eval(technical_message.content)
        sentiment_signals = ast.literal_eval(sentiment_message.content)
        
    agent_signals = {
        "technical": technical_signals,
        "sentiment": sentiment_signals,
    }

    # 1. Calculate volatility
    prices_df['returns'] = prices_df['close'].pct_change()
    prices_df.dropna(inplace=True)
    volatility = prices_df['returns'].std()  
    



    # 2. Position Size Limits
    max_loss_cash = cash * max_loss
    max_position_size = max_loss_cash / volatility
    if (max_position_size > cash):
        max_position_size = cash
    
    #3. Stop loss, Price Stop Loss
    stop_loss = "{:.2%}".format(volatility)






    message_content = {
        "max_position_size": float(max_position_size),
        "risk_metrics": {
            "volatility": float(volatility),
            "stop loss" : stop_loss,

        },
        "reasoning": f"Volatility={volatility:.2%},  "
                     f"Max Loss as a percentage of the fund={max_loss:.2%} , "
                     f"Max Loss as cash of the fund={max_loss_cash:.2%}"
                     
    }

    # Create the risk management message
    message = HumanMessage(
        content=json.dumps(message_content),
        name="risk_management_agent",
    )

    if show_reasoning:
        show_agent_reasoning(message_content, "Risk Management Agent")

    return {"messages": state["messages"] + [message]}


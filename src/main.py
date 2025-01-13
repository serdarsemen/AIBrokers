from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from agents.market_data import market_data_agent, check_data_valid
from agents.portfolio_manager import portfolio_management_agent
from agents.technicals import technical_analyst_agent
from agents.risk_manager import risk_management_agent
from agents.sentiment import sentiment_agent
from agents.state import AgentState

import argparse
from datetime import datetime





##### Run the AIBrokers #####
def run_hedge_fund(crypto: str, start_date: str, end_date: str, portfolio: dict, show_reasoning: bool = False):
    valid = check_data_valid(crypto,start_date, end_date)
    if valid:
        final_state = app.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="Make a trading decision based on the provided data.",
                    )
                ],
                "data": {
                    "crypto": crypto,
                    "portfolio": portfolio,
                    "start_date": start_date,
                    "end_date": end_date,
                    "analyst_signals": {},
                },
                "metadata": {
                    "show_reasoning": show_reasoning,
                }
            },
        )
        return final_state["messages"][-1].content
    else:
        return "Cant Run AI"

# Define the new workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("market_data_agent", market_data_agent)
workflow.add_node("technical_analyst_agent", technical_analyst_agent)
workflow.add_node("sentiment_agent", sentiment_agent)
workflow.add_node("risk_management_agent", risk_management_agent)
workflow.add_node("portfolio_management_agent", portfolio_management_agent)

# Define the workflow
workflow.set_entry_point("market_data_agent")
workflow.add_edge("market_data_agent", "technical_analyst_agent")
workflow.add_edge("market_data_agent", "sentiment_agent")
workflow.add_edge("technical_analyst_agent", "risk_management_agent")
workflow.add_edge("sentiment_agent", "risk_management_agent")
workflow.add_edge("risk_management_agent", "portfolio_management_agent")
workflow.add_edge("portfolio_management_agent", END)

app = workflow.compile()

# Add this at the bottom of the file
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the hedge fund trading system')
    parser.add_argument('--crypto', type=str, required=True, help='Stock crypto symbol')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD). Defaults to 1 months before end date')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD). Defaults to today')
    parser.add_argument('--show-reasoning', action='store_true', help='Show reasoning from each agent')
    
    args = parser.parse_args()

    # Validate dates if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")
    
    if args.end_date:
        try:
            datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")
    
    # Sample portfolio - you might want to make this configurable too
    portfolio = {
        "cash": 100000.0,  # $100,000 initial cash
        
    }
    
    result = run_hedge_fund(
        crypto=args.crypto,
        start_date=args.start_date,
        end_date=args.end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning
    )
    print("\nFinal Result:")
    print(result)
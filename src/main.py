from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
import os
from agents.market_data import market_data_agent, check_data_valid
from agents.portfolio_manager import portfolio_management_agent
from agents.technicals import technical_analyst_agent
from agents.risk_manager import risk_management_agent
from agents.sentiment import sentiment_agent
from agents.state import AgentState
import argparse
from datetime import datetime

def select_llm_provider():
    """Display menu for LLM provider selection and return choice"""
    while True:
        print("\nSelect LLM Provider:")
        print("1. OpenAI")
        print("2. Azure OpenAI")
        print("3. Groq")
        print("4. Google Gemini")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            if not os.getenv("OPENAI_API_KEY"):
                print("\nError: OPENAI_API_KEY not found in environment variables.")
                print("Please set it in your .env file and try again.")
                continue
            os.environ["LLM_PROVIDER"] = "openai"
            return "openai"

        elif choice == "2":
            required_vars = [
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_DEPLOYMENT_NAME",
                "AZURE_OPENAI_API_VERSION"
            ]

            missing_vars = [var for var in required_vars if not os.getenv(var)]

            if missing_vars:
                print("\nError: Missing required Azure OpenAI environment variables:")
                for var in missing_vars:
                    print(f"- {var}")
                print("Please set them in your .env file and try again.")
                continue

            os.environ["LLM_PROVIDER"] = "azure"
            return "azure"

        elif choice == "3":
            if not os.getenv("GROQ_API_KEY"):
                print("\nError: GROQ_API_KEY not found in environment variables.")
                print("Please set it in your .env file and try again.")
                continue
            os.environ["LLM_PROVIDER"] = "groq"
            return "groq"

        elif choice == "4":
            if not os.getenv("GOOGLE_API_KEY"):
                print("\nError: GOOGLE_API_KEY not found in environment variables.")
                print("Please set it in your .env file and try again.")
                continue
            os.environ["LLM_PROVIDER"] = "gemini"
            return "gemini"

        else:
            print("\nInvalid choice. Please select 1-4.")

##### Run the AIBrokers #####
def run_hedge_fund(
    crypto: str,
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
):
    """Run the AI-powered hedge fund trading system.

    Args:
        crypto: Symbol of the cryptocurrency to trade
        start_date: Start date for analysis (YYYY-MM-DD)
        end_date: End date for analysis (YYYY-MM-DD)
        portfolio: Dictionary containing portfolio information:
            - cash: Available capital
            - leverage: Trading leverage
            - risk: Risk tolerance per trade
        show_reasoning: Whether to display agent reasoning

    Returns:
        str: Trading decision in JSON format containing action and quantity
    """
    valid = check_data_valid(crypto, start_date, end_date)
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
                },
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

if __name__ == "__main__":
    print("\nWelcome to AIBrokers Trading System")
    print("===================================")

    # Select LLM provider before parsing arguments
    selected_provider = select_llm_provider()
    print(f"\nUsing {selected_provider.upper()} as LLM provider")

    parser = argparse.ArgumentParser(description="Run the hedge fund trading system")
    parser.add_argument("--crypto", type=str, required=True, help="Stock crypto symbol")
    parser.add_argument(
        "--balance",
        type=float,
        help="Your balance available to trade. Default: 100000$",
    )
    parser.add_argument(
        "--leverage", type=float, help="Leverage you want to set. Default: 10"
    )
    parser.add_argument(
        "--risk",
        type=float,
        help="Proportion of the total balance that can be lost per trade. Default: 0.05",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date (YYYY-MM-DD). Defaults to 1 months before end date",
    )
    parser.add_argument(
        "--end-date", type=str, help="End date (YYYY-MM-DD). Defaults to today"
    )
    parser.add_argument(
        "--show-reasoning", action="store_true", help="Show reasoning from each agent"
    )

    args = parser.parse_args()

    # Validate dates if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")

    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")

    portfolio = {"cash": args.balance, "leverage": args.leverage, "risk": args.risk}
    if not args.balance:
        portfolio["cash"] = 100000
    if not args.leverage:
        portfolio["leverage"] = 10
    if not args.risk:
        portfolio["risk"] = 0.05

    result = run_hedge_fund(
        crypto=args.crypto,
        start_date=args.start_date,
        end_date=args.end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning,
    )
    print("\nFinal Result:")
    print(result)

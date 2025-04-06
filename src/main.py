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

def get_model_name(provider):
    """Return the model name based on the selected provider."""
    if provider == "openai":
        return "gpt-4"
    elif provider == "azure":
        return os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    elif provider == "groq":
        return os.getenv("GROQ_MODEL_NAME")  # or whichever model Groq uses
    elif provider == "gemini":
        return os.getenv("GOOGLE_MODEL_NAME")
    else:
        return "unknown model"

def validate_provider_env_vars(provider: str) -> tuple[bool, list[str]]:
    """Validate environment variables for given provider

    Returns:
        (bool, list): (is_valid, missing_vars)
    """
    required_vars = {
        "openai": ["OPENAI_API_KEY"],
        "azure": [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION"
        ],
        "groq": ["GROQ_API_KEY"],
        "gemini": ["GOOGLE_API_KEY"]
    }

    vars_needed = required_vars.get(provider, [])
    missing = [var for var in vars_needed if not os.getenv(var)]
    return (len(missing) == 0, missing)

def select_llm_provider():
    """Display menu for LLM provider selection and return choice"""
    while True:
        print("\nSelect LLM Provider:")
        print("1. OpenAI")
        print("2. Azure OpenAI")
        print("3. Groq")
        print("4. Google Gemini")

        choice = input("Enter your choice (1-4): ").strip()

        providers = {
            "1": "openai",
            "2": "azure",
            "3": "groq",
            "4": "gemini"
        }

        if choice not in providers:
            print("\nInvalid choice. Please select 1-4.")
            continue

        provider = providers[choice]
        is_valid, missing_vars = validate_provider_env_vars(provider)

        if not is_valid:
            print(f"\nError: Missing required environment variables for {provider}:")
            for var in missing_vars:
                print(f"- {var}")
            print("Please set them in your .env file and try again.")
            continue

        os.environ["LLM_PROVIDER"] = provider
        return provider

##### Run the AIBrokers #####
def run_hedge_fund(
    crypto: str,
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
) -> str:
    """Run the AI-powered hedge fund trading system."""
    if not check_data_valid(crypto, start_date, end_date):
        return "Cannot Run AI - Invalid Data"

    initial_state = {
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
    }

    try:
        final_state = APP.invoke(initial_state)
        return final_state["messages"][-1].content
    except Exception as e:
        return f"Error running AI: {str(e)}"


# Define the new workflow
WORKFLOW = StateGraph(AgentState)
WORKFLOW.add_node("market_data_agent", market_data_agent)
WORKFLOW.add_node("technical_analyst_agent", technical_analyst_agent)
WORKFLOW.add_node("sentiment_agent", sentiment_agent)
WORKFLOW.add_node("risk_management_agent", risk_management_agent)
WORKFLOW.add_node("portfolio_management_agent", portfolio_management_agent)

# Define the workflow once
WORKFLOW.set_entry_point("market_data_agent")
WORKFLOW.add_edge("market_data_agent", "technical_analyst_agent")
WORKFLOW.add_edge("market_data_agent", "sentiment_agent")
WORKFLOW.add_edge("technical_analyst_agent", "risk_management_agent")
WORKFLOW.add_edge("sentiment_agent", "risk_management_agent")
WORKFLOW.add_edge("risk_management_agent", "portfolio_management_agent")
WORKFLOW.add_edge("portfolio_management_agent", END)

APP = WORKFLOW.compile()

def validate_date(date_str: str, date_type: str) -> None:
    """Validate date format

    Args:
        date_str: Date string to validate
        date_type: 'start' or 'end' for error message

    Raises:
        ValueError: If date format is invalid
    """
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as err:
            raise ValueError(f"{date_type} date must be in YYYY-MM-DD format") from err

DEFAULT_PORTFOLIO = {
    "cash": 100000,
    "leverage": 10,
    "risk": 0.05
}

def create_portfolio(args) -> dict:
    """Create portfolio with defaults if needed"""
    return {
        "cash": args.balance or DEFAULT_PORTFOLIO["cash"],
        "leverage": args.leverage or DEFAULT_PORTFOLIO["leverage"],
        "risk": args.risk or DEFAULT_PORTFOLIO["risk"]
    }

if __name__ == "__main__":
    print("\nWelcome to AI Coin Trading System")
    print("===================================")

    # Select LLM provider before parsing arguments
    selected_provider = select_llm_provider()
    model_name = get_model_name(selected_provider)
    print(f"\nUsing {selected_provider.upper()} as LLM provider")
    print(f"Model: {model_name}")

    parser = argparse.ArgumentParser(description="Run the hedge fund trading system")
    parser.add_argument("--crypto", type=str, required=True, help="Crypto symbol")
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

    validate_date(args.start_date, "Start")
    validate_date(args.end_date, "End")

    portfolio = create_portfolio(args)
    result = run_hedge_fund(
        crypto=args.crypto,
        start_date=args.start_date,
        end_date=args.end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning,
    )
    print("\nFinal Result:")
    print(result)

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

from main import run_hedge_fund
from tools.api import get_price_API_BINANCE

class Backtester:
    def __init__(self, agent, crypto, start_date, end_date, initial_capital):
        self.agent = agent
        self.crypto = crypto
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.portfolio = {"cash": initial_capital, "collateral_long": 0, "collateral_short" : 0, "price_collateral" : 0}
        self.portfolio_values = []

    def parse_action(self, agent_output):
        try:
            # Expect JSON output from agent
            import json
            decision = json.loads(agent_output)
            return decision["action"], decision["quantity"]
        except:
            print(f"Error parsing action: {agent_output}")
            return "hold", 0

    def execute_trade(self, action, quantity, current_price):
        """Validate and execute trades based on portfolio constraints"""
        if action == "long" and quantity > 0:
            
            if (self.portfolio['cash'] >= quantity):
                collateral  = round(quantity/current_price,2)
                self.portfolio["collateral_long"] += collateral
                self.portfolio['cash'] -= quantity
                self.portfolio["price_collateral"]=current_price
                
                

                
                
            

            
        elif action == "short" and quantity > 0:
            
            if (self.portfolio['cash'] > quantity):
                collateral  = round(quantity/current_price,2)
                self.portfolio["collateral_short"] += collateral
                self.portfolio['cash'] -= quantity
                self.portfolio["price_collateral"]=current_price
                
        return quantity
    
    def sell_collateral(self, current_price):
        if self.portfolio["collateral_short"] != 0 :
            cash_out = self.portfolio["collateral_short"]  * ( 2 *self.portfolio["price_collateral"] -current_price )
            
            self.portfolio["cash"] += cash_out
            self.portfolio["collateral_short"] = 0
        if self.portfolio["collateral_long"] != 0 :
            cash_out = self.portfolio["collateral_long"]  * current_price 
            self.portfolio["cash"] += cash_out 
            self.portfolio["collateral_long"] = 0
        pass

    def run_backtest(self):
        dates = pd.date_range(self.start_date, self.end_date, freq="B")

        print("\nStarting backtest...")
        print(f"{'Date':<12} {'Crypto':<6} {'Action':<6} {'Quantity':>8} {'Price':>8} {'Cash':>12} {'Collateral long':>8} {'Collateral short':>8} {'Total Value':>12}")
        print("-" * 100)

        for current_date in dates:
            lookback_start = (current_date - timedelta(days=30)).strftime("%Y-%m-%d")
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            df = get_price_API_BINANCE(self.crypto, lookback_start, current_date_str)
            current_price = df.iloc[-1]['close']
            
            self.sell_collateral(current_price)
            
            agent_output = self.agent(
                crypto=self.crypto,
                start_date=lookback_start,
                end_date=current_date_str,
                portfolio=self.portfolio
            )
            

            action, quantity = self.parse_action(agent_output)           

            

            # Execute the trade with validation
            executed_quantity = self.execute_trade(action, quantity, current_price)

            # Update total portfolio value
            if ( self.portfolio["collateral_long"] > 0):                
                total_value = self.portfolio["cash"] + self.portfolio["collateral_long"]  * current_price 
            elif(self.portfolio["collateral_short"] > 0):
                total_value = self.portfolio["cash"] + self.portfolio["collateral_short"]  * ( 2 *self.portfolio["price_collateral"] -current_price )
            else:
                total_value = self.portfolio["cash"]
            self.portfolio["portfolio_value"] = total_value

            # Log the current state with executed quantity
            print(
                f"{current_date.strftime('%Y-%m-%d'):<12} {self.crypto:<6} {action:<6} {executed_quantity:>8} {current_price:>8.2f} "
                f"{self.portfolio['cash']:>12.2f} {self.portfolio['collateral_long']:>8} {self.portfolio['collateral_short']:>8} {total_value:>12.2f}"
            )

            # Record the portfolio value
            self.portfolio_values.append(
                {"Date": current_date, "Portfolio Value": total_value}
            )

    def analyze_performance(self):
        # Convert portfolio values to DataFrame
        performance_df = pd.DataFrame(self.portfolio_values).set_index("Date")

        # Calculate total return
        total_return = (
                           self.portfolio["portfolio_value"] - self.initial_capital
                       ) / self.initial_capital
        print(f"Total Return: {total_return * 100:.2f}%")

        # Plot the portfolio value over time
        performance_df["Portfolio Value"].plot(
            title="Portfolio Value Over Time", figsize=(12, 6)
        )
        plt.ylabel("Portfolio Value ($)")
        plt.xlabel("Date")
        plt.show()

        # Compute daily returns
        performance_df["Daily Return"] = performance_df["Portfolio Value"].pct_change()

        # Calculate Sharpe Ratio (assuming 252 trading days in a year)
        mean_daily_return = performance_df["Daily Return"].mean()
        std_daily_return = performance_df["Daily Return"].std()
        sharpe_ratio = (mean_daily_return / std_daily_return) * (252 ** 0.5)
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

        # Calculate Maximum Drawdown
        rolling_max = performance_df["Portfolio Value"].cummax()
        drawdown = performance_df["Portfolio Value"] / rolling_max - 1
        max_drawdown = drawdown.min()
        print(f"Maximum Drawdown: {max_drawdown * 100:.2f}%")

        return performance_df
    
### 4. Run the Backtest #####
if __name__ == "__main__":
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run backtesting simulation')
    parser.add_argument('--crypto', type=str, help='collateral crypto symbol (e.g., AAPL)')
    parser.add_argument('--end-date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date in YYYY-MM-DD format')
    parser.add_argument('--start-date', type=str, default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), help='Start date in YYYY-MM-DD format')
    parser.add_argument('--initial-capital', type=float, default=100000, help='Initial capital amount (default: 100000)')

    args = parser.parse_args()

    # Create an instance of Backtester
    backtester = Backtester(
        agent=run_hedge_fund,
        crypto=args.crypto,
        start_date=args.start_date,
        end_date=args.end_date,
        initial_capital=args.initial_capital,
    )

    # Run the backtesting process
    backtester.run_backtest()
    performance_df = backtester.analyze_performance()

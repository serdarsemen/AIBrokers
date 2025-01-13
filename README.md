# AIBrokers

The first real-world AI hedge fund framework in crypto, fully open source!
AIBrokers is a framework designed to create multi AI agents for managing hedge funds. These AI agents act as professional traders, operating 24/7 to manage investments for their owners. My vision and aspiration are that, with unlimited contributions from the community, AIBrokers can outperform hedge funds, whales, and market makers in the future. AIBrokers is open source and welcomes contributions from anyone.


This system employs several agents working together:
- Trader Behavior Agent: Gather on-chain trader behavior, traders actions, etc.
- Quant Agent: calculates signals like MACD, RSI, Bollinger Bands, etc.
- Sentiment Agent: gathers, analyzes crypto market sentiment from social media, news, and on-chain data to support trading strategies, etc.
- Fundamental Agent: evaluates crypto projects' tokenomics, on-chain data, market performance, and ecosystem to guide long-term investment decisions, etc.
- Technical Analyst Agent: analyzes crypto price charts, trends, and indicators to identify trading opportunities and optimize entry/exit points, etc.
- Rish manager: assesses market volatility, portfolio exposure, and potential risks to minimize losses and optimize risk-reward ratios.
- Fund Manager Agent: makes final trading decisions and generates orders, etc.


Note: the system simulates trading decisions, it does not actually trade.

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No warranties or guarantees provided
- Past performance does not indicate future results
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions

By using this software, you agree to use it solely for learning purposes.



## Setup

Clone the repository:
```bash
git clone https://github.com/AI-Brokers/AIBrokers0.0.1.git


```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env

export OPENAI_API_KEY='your-api-key-here' # Get a key from https://platform.openai.com/
```

## Usage

### Running the AIBrokers

```bash
poetry run python src/main.py --crypto BTC
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
poetry run python src/main.py --crypto BTC --show-reasoning
```
You can optionally specify the start and end dates to make decisions for a specific time period.

```bash
poetry run python src/main.py --crypto BTC --start-date 2024-01-01 --end-date 2024-03-01 
```

### Running the Backtester

```bash
poetry run python src/backtester.py --crypto BTC
```

**Example Output:**
```
Starting backtest...
Date         Crypto Action Quantity    Price         Cash    colatteralLong collateralShort  Total Value
-----------------------------------------------------------------------------------------------------------
2024-12-16   BTC    long     100000 103124.30         0.00     0.97             0              100030.57
2024-12-17   BTC    short    103816 107026.90         0.09        0             0.97           103816.19
2024-12-18   BTC    long     103397 107458.50         0.53     0.96             0              103160.69
2024-12-19   BTC    long     100433 104617.30         0.14     0.96             0              100432.75
2024-12-20   BTC    short     94863 98815.90          0.41        0             0.96            94863.67
```

You can optionally specify the start and end dates to backtest over a specific time period.

```bash
poetry run python src/backtester.py --crypto BTC --start-date 2024-01-01 --end-date 2024-03-01
```

## Project Structure 
```
AIBrokers/
├── src/
│   ├── agents/                   # Agent definitions and workflow│  
│   │   ├── market_data.py        # Market data agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── state.py              # Agent state
│   │   ├── technicals.py         # Technical analysis agent│  
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py # Main entry point
├── pyproject.toml
├── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Usercase
- Chat Box/ Social Bot/ Signal Bot
- The Autonomous AI-Driven Hedge Fund
- AI-Powered Copilot Trading Assistant
## Community
- X: https://x.com/aibrokers_xyz
- Discord: https://discord.gg/fsvxUZJ2
- Media Kit: https://drive.google.com/drive/folders/1SKjgkHd0j-iClgCxsuVcYfHyxB-cvqhI?usp=sharing

---
- Schema Inspired: https://github.com/virattt/ai-hedge-fund

## License

This project is licensed under the MIT License - see the LICENSE file for details.

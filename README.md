# AIBrokers

The first real-world AI hedge fund framework in crypto, fully open source!
AIBrokers is a framework designed to create multi AI agents for managing hedge funds. These AI agents act as professional traders, operating 24/7 to manage investments for their owners. My vision and aspiration are that, with unlimited contributions from the community, AIBrokers can outperform hedge funds, whales, and market makers in the future. AIBrokers is open source and welcomes contributions from anyone.


<img width="1060" alt="Screenshot 2025-01-03 at 5 39 25 PM" src="https://github.com/user-attachments/assets/9070ed76-7156-4b65-a3a5-079b605f3110" />


This system employs several agents working together:
- Trader Behavior Agent: Gather on-chain trader behavior, traders actions, etc.
- Quant Agent: calculates signals like MACD, RSI, Bollinger Bands, etc.
- Sentiment Agent: gathers, analyzes crypto market sentiment from social media, news, and on-chain data to support trading strategies, etc.
- Fundamental Agent: evaluates crypto projects' tokenomics, on-chain data, market performance, and ecosystem to guide long-term investment decisions, etc.
- Technical Analyst Agent: analyzes crypto price charts, trends, and indicators to identify trading opportunities and optimize entry/exit points, etc.
- Risk manager: assesses market volatility, portfolio exposure, and potential risks to minimize losses and optimize risk-reward ratios.
- Fund Manager Agent: makes final trading decisions and generates orders, etc.


Note: the system simulates trading decisions, it does not actually trade.





## Setup

Clone the repository:
```bash
git clone https://github.com/AI-Brokers/AIBrokers.git


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
**Example Output:**
<img width="992" alt="Screenshot 2025-01-06" src="https://github.com/user-attachments/assets/1fb088d8-7924-4c70-9f9b-dfe0d721f161" />

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



## Usercase
- Chat Box/ Social Bot/ Signal Bot
- The Autonomous AI-Driven Hedge Fund
- AI-Powered Copilot Trading Assistant
## Community
- X: https://x.com/aibrokers_xyz
- Discord: https://discord.gg/zQpKw6eeQu
- Media Kit: https://drive.google.com/drive/folders/1SKjgkHd0j-iClgCxsuVcYfHyxB-cvqhI?usp=sharing

---
- Schema Inspired: https://github.com/virattt/ai-hedge-fund


## Challenges/Task
Here’s a structured **to-do list** to request contributions from the community for the AIBrokers open-source project. It includes both **challenges** and **tasks** to inspire developers to contribute meaningfully:

### **1\. Core System Architecture**

*   **Define and document APIs** for communication between agents (e.g., Trader Behavior Agent ↔ Fund Manager Agent).
    
*   **Implement agent orchestration**: Develop a modular framework to coordinate multiple agents effectively.
    
*   **Set up a backtesting environment** for simulated trading strategies to validate AI decisions.
    

### **2\. Trader Behavior Agent**

*   Build a scraper to gather **on-chain trader behavior data** (e.g., wallet actions, trading volume).
    
*   Implement **anomaly detection** for unusual trading patterns.
    
*   Develop tools for **visualizing trader behavior trends**.
    

### **3\. Quant Agent**

*   Implement advanced indicators (e.g., **MACD**, **RSI**, **Bollinger Bands**, **Ichimoku Cloud**).
    
*   Create a **signal combination engine** for multi-indicator strategies.
    
*   Integrate with live and historical price data APIs (e.g., Binance, Kraken).
    

### **4\. Sentiment Agent**

*   Develop a **social media sentiment analyzer** using NLP (Twitter, Reddit, Telegram, etc.).
    
*   Incorporate on-chain data for **community sentiment trends** (e.g., token transfers).
    
*   Build a dashboard for **sentiment visualization** with real-time updates.
    

### **5\. Fundamental Agent**

*   Design a scoring model for evaluating tokenomics (e.g., **inflation rate**, **supply schedule**).
    
*   Analyze crypto ecosystems and detect **growth opportunities**.
    
*   Build tools for **tracking developer activity** on GitHub and other repositories.
    

### **6\. Technical Analyst Agent**

*   Develop AI models to predict price trends based on historical chart patterns.
    
*   Implement multi-timeframe analysis (e.g., **15m, 1H, daily** charts).
    
*   Automate **entry and exit signal generation** based on technical indicators.
    

### **7\. Risk Manager**

*   Build a module to calculate **portfolio exposure** and suggest optimal rebalancing.
    
*   Develop algorithms for **stop-loss and take-profit management**.
    
*   Implement a **stress testing** tool for simulating market crashes.
    

### **8\. Fund Manager Agent**

*   Create a **decision-making engine** to rank and execute agent recommendations.
    
*   Develop an order simulation system (e.g., buy/sell orders with slippage considerations).
    
*   Allow customizable strategies: e.g., risk tolerance, aggressive vs. conservative.
    

### **9\. Infrastructure & Scalability**

*   Migrate data pipelines to a scalable **distributed system** (e.g., Kafka, RabbitMQ).
    
*   Ensure agent modularity to support **plug-and-play integration**.
    
*   Containerize the framework using **Docker** for easy deployment.
    

### **10\. Community Contributions**

*   Build **detailed contributing guidelines** (e.g., coding standards, testing requirements).
    
*   Open a list of **Good First Issues** for new contributors.
    
*   Encourage building **plugins or extensions** for specific strategies.
    

### **11\. Challenges for the Community**

*   How can AI agents detect **manipulated or wash-traded tokens**?
    
*   What’s the best way to optimize **multi-agent collaboration** for decision-making?
    
*   Can reinforcement learning improve trading strategy performance over time?
    
*   How do we handle **low-liquidity markets** effectively?
    

### **12\. Documentation and Knowledge Sharing**

*   Write **clear documentation** for each agent, its role, and integration process.
    
*   Publish examples of **successful backtests** to showcase the system's potential.
    
*   Create video tutorials to onboard developers.
    

By addressing these areas, the project can attract developers of varying skill levels to contribute and grow AIBrokers into a comprehensive framework.



## License

This project is licensed under the MIT License - see the LICENSE file for details.

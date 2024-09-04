Momentum-Based Trading Strategy
Overview
This trading strategy focuses on selecting stocks based on their momentum and volatility, with the goal of maintaining a portfolio of high-performing stocks while managing risk through position sizing and regular rebalancing. The strategy has three versions that differ in how frequently positional data is updated and how often rebalancing occurs.

Key Principles
Avoid Buying in a Bear Market: Only buy stocks when the chosen index (Nifty 500, Nifty Midcap 400, or Nifty Smallcap 500) is above its 200-day SMA.

Stock Selection:

Rank stocks based on volatility and momentum using the last 90 days of data.
Calculate the slope and R² of the stock's price using rolling 90-day data.
Convert the slope into an annualized return and adjust it using R².
Rank stocks based on this adjusted annualized return.
Only consider stocks above their 100-day SMA and exclude any stock with a move larger than 15% in the past 90 days.
Select the top 30 stocks based on these criteria.

Position Sizing:
1. Use the Average True Range (ATR) calculated over 20 days to determine position size.
2. Position size is calculated as: Shares = [Account Value * Risk Factor] / ATR, where Risk Factor = 0.1%.
3. Rebalance position sizes to maintain consistent risk allocation bi-weekly or monthly.

Portfolio Maintenance:
Stocks must be in the top 20% of the Nifty 500 universe to remain in the portfolio.
Remove stocks that fall out of the top 20% or trade below their 100-day SMA.
Rebalance the portfolio by removing disqualified stocks and repeating the selection cycle.
Strategy Versions

Version 1: Weekly Positional Data
    Selling: Daily.
    New Buying: Weekly.
    Rebalancing: Weekly.

Version 2: Bi-Weekly Positional Data
    Selling: Daily.
    New Buying: Weekly.
    Rebalancing: Bi-Weekly.

Version 3: Monthly Positional Data
    Selling: Daily.
    New Buying: Weekly.
    Rebalancing: Monthly.
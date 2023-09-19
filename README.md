# Option Pricing Model in Python

An option pricing model in Python that calculates theoretical prices for both call and put options using the Black-Scholes formula and the binomial model. It gathers current market data, computes historical volatility, and uses the SONIA overnight rate for the risk-free rate estimations. Supports user inputs for strike price and expiration date. 

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Functions Overview](#functions-overview)

## Features

- **Black-Scholes Model:** The program calculates both call and put option prices using the renowned Black-Scholes formula.
- **Binomial Model:** Alongside Black-Scholes, the program also uses a binomial model to evaluate option prices
- **Real-time Data Integration:** The program fetches current market prices and historical volatility using the yfinance library. Furthermore, the SONIA overnight rate is retrieved using the 'quandl' library as an estimate for the risk-free rate.

## Prerequisites

To install the required libraries, run the following command: 

```
pip install -r requirements.txt
```

## Usage

1. Run main.py
2. Input the ticker symbol for the underlying asset
3. Follow the prompts to enter further details such as the option's strike price and expiration date
4. The program will display the call and put prices for the Black-Scholes model as well as the binomial model

## Functions Overview
- **get_contract_data:** Gathers necessary data for option pricing
- **get_current_market_data:** Fetches the current market price for a specified ticker
- **calculate_time_to_expiration:** Calculates the time to option expiration based on user input
- **calculate_volatility:** Calculates historical volatility
- **get_risk_free_rate:** Fetches the SONIA overnight rate as a risk-free rate estimate
- **calculate_d1_bs** & **calculate_d2_bs:** Calculates d1 and d2 values for the Black-Scholes formula
- **bs_call_value** & **bs_put_value:** Computes call and put option prices using the Black-Scholes formula
- **binomial_model:** Computes option prices using the binomial model
  

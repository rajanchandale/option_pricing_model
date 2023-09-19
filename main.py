import numpy as np
import yfinance as yf
import quandl
import datetime
import math
from scipy.stats import norm


def get_contract_data(ticker):
    """
    Gather necessary data for option pricing based on user inputs and external data sources

    Parameters:
        - ticker (str): Ticker symbol for the underlying asset

    Returns:
        - tuple: A tuple containing strike price, current market price, time to expiration, volatility,
        and risk-free rate
    """
    strike_price = float(input("STRIKE PRICE: "))
    current_market_price = get_current_market_price(ticker)
    time_to_expiration = calculate_time_to_expiration()
    volatility = calculate_volatility(ticker)
    risk_free_rate = get_risk_free_rate()

    return strike_price, current_market_price, time_to_expiration, volatility, risk_free_rate


def get_current_market_price(ticker):
    """
    Fetch the current market price for the specified ticker

    Parameters:
        - ticker (str): Ticker symbol for the underlying asset

    Returns:
        - float: The current market price
    """
    start_date = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    market_data = yf.download(ticker, start=start_date, end=end_date)

    print("MARKET DATA: ", market_data)

    print("CURRENT MARKET PRICE: ", market_data['Adj Close'].iloc[-1])

    return market_data['Adj Close'].iloc[-1]


def calculate_time_to_expiration():
    """
    Calculate the time to option expiration based on user input

    Returns:
        - float: Time to expiration in years
    """
    expiry_year = int(input("PLEASE ENTER THE YEAR THE OPTION EXPIRES: "))
    expiry_month = int(input("PLEASE ENTER THE MONTH THE OPTION EXPIRES: "))
    expiry_day = int(input("PLEASE ENTER THE DAY THE OPTION EXPIRES: "))

    expiry_date = datetime.datetime(expiry_year, expiry_month, expiry_day)

    today_date = datetime.datetime.now()

    time_to_expiration = (expiry_date - today_date).days / 365.0
    print("TIME: ",time_to_expiration)

    return time_to_expiration


def calculate_volatility(ticker):
    """
    Calculate the historical volatility for the specified icker value

    Parameters:
        - ticker (str): Ticker symbol for the underlying asset

    Returns:
        - float: The historical volatility
    """
    start_date = (datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    historical_data = yf.download(ticker, start=start_date, end=end_date)

    daily_returns = historical_data['Adj Close'].pct_change()

    volatility = np.std(daily_returns)
    print("VOLATILITY: ", volatility)

    return volatility


def get_risk_free_rate():
    """
    Fetch the SONIA overnight rate as an estimate for the risk-free rate

    Returns:
        - float: The risk-free rate
    """
    quandl.ApiConfig.api_key = "<your-api-key>"

    sonia_data = quandl.get("BOE/IUDSNPY", rows=1)
    risk_free_rate = sonia_data['Value'].iloc[0] / 100
    print("RISK FREE RATE: ", risk_free_rate)

    return risk_free_rate


def calculate_d1_bs(strike_price, current_market_price, time_to_expiration, risk_free_rate, volatility):
    """
    Calculate the d1 value for the Black-Scholes option pricing formula

    Parameters:
        - strike_price (float): The strike price of the option
        - current_market_price (float): The current price of the underlying asset
        - time_to_expiration (float): The time to expiration of the option in years
        - risk_free_rate (float): Current risk-free interest rate
        - volatility (float): Historical volatility of the underlying asset

    Returns:
        - float: The d1 value
    """
    numerator = math.log(current_market_price / strike_price) + \
                ((risk_free_rate + 0.5 * (volatility**2))*time_to_expiration)

    denominator = volatility * math.sqrt(time_to_expiration)

    print("d1: ", numerator/denominator)

    return numerator/denominator


def calculate_d2_bs(d1, volatility, time_to_expiration):
    """
    Calculate the d2 value based on the d1 value for the Black-Scholes formula

    Parameters:
        - d1 (float): The d1 value calculated from the Black-Scholes formula
        - volatility (float): Historical volatility of the underlying asset
        - time_to_expiration (float): Time to expiration of the option in years

    Returns:
        - float: The d2 value
    """
    d2 = d1 - (volatility * math.sqrt(time_to_expiration))
    print("D2: ", d2)

    return d2


def bs_call_value(strike_price, current_market_price, time_to_expiration, risk_free_rate, d1, d2):
    """
    Compute the call option price using the Black-Scholes formula

    Parameters:
        - strike_price (float): The strike price of the option
        - current_market_price (float): The current price of the underlying asset
        - time_to_expiration (float): The time to expiration of the option in years
        - risk_free_rate (float): Current risk-free interest rate
        - d1 (float): The d1 value calculated from the Black-Scholes formula
        - d2 (float): The d2 value calculated from the Black-Scholes formula

    Returns:
        - float: Price of the call option
    """
    call_price = (current_market_price * norm.cdf(d1)) -\
                 (norm.cdf(d2) * strike_price * math.exp(-risk_free_rate * time_to_expiration))

    return call_price


def bs_put_value(strike_price, current_market_price, time_to_expiration, risk_free_rate, d1, d2):
    """
    Compute the put option price using the Black-Scholes formula

    Parameters:
        - strike_price (float): The strike price of the option
        - current_market_price (float): The current price of the underlying asset
        - time_to_expiration (float): Time to expiration of the option in years
        - risk_free_rate (float): Current risk-free interest rate
        - d1 (float): The d1 value calculated from the Black-Scholes formula
        - d2 (float): The d2 value calculated from the Black-Scholes formula

    Returns:
        - float: Price of the put option
    """
    put_price = (strike_price * math.exp(-risk_free_rate*time_to_expiration) * norm.cdf(-d2)) -\
                (current_market_price * norm.cdf(-d1))

    return put_price


def binomial_model(strike_price, current_market_price, time_to_expiration, risk_free_rate, volatility, num_intervals):
    """
    Compute option prices using the binomial model

    Parameters:
        - strike_price (float): The strike price of the option
        - current_market_price (float):The current price of the underlying asset
        - time_to_expiration (float): Time to expiration of the option in years
        - risk_free_rate (float): Current risk-free interest rate
        - volatility (float): Historical volatility of the underlying asset
        - num_intervals (int): Number of intervals for the binomial tree

    Returns:
        - tuple: Price of the call and put options
    """
    def combos(num_intervals, i):
        return math.factorial(num_intervals) / (math.factorial(num_intervals-i)*math.factorial(i))

    time_intervals = time_to_expiration / num_intervals

    u = np.exp(volatility * np.sqrt(time_intervals))
    d = np.exp(-volatility * np.sqrt(time_intervals))
    p = (np.exp(risk_free_rate*time_intervals) - d) / (u - d)

    call_value = 0
    put_value = 0
    for i in range(num_intervals+1):
        node_probability = combos(num_intervals, i)*p**i*(1-p)**(num_intervals-i)
        st = current_market_price*(u)**i*(d)**(num_intervals-i)
        call_value += max(st-strike_price, 0) * node_probability
        put_value += max(strike_price-st, 0) * node_probability

    return call_value*np.exp(-risk_free_rate*time_to_expiration), put_value*np.exp(-risk_free_rate*time_to_expiration)


def main():
    """
    Main code execution. Retrieves and displays option prices using the above functions
    """
    ticker = input("ENTER TICKER: ")
    print("CURRENT MARKET PRICE: ", get_current_market_price(ticker))
    strike_price, current_market_price, time_to_expiration, volatility, risk_free_rate = get_contract_data(ticker)
    d1 = calculate_d1_bs(strike_price, current_market_price, time_to_expiration, risk_free_rate, volatility)
    d2 = calculate_d2_bs(d1, volatility, time_to_expiration)
    call_price = bs_call_value(strike_price, current_market_price, time_to_expiration, risk_free_rate, d1, d2)
    put_price = bs_put_value(strike_price, current_market_price, time_to_expiration, risk_free_rate, d1, d2)

    print("CALL PRICE: ", round(call_price, 2))
    print("PUT PRICE: ", round(put_price, 2))

    binomial_call_value, binomial_put_value = binomial_model(strike_price, current_market_price, time_to_expiration,
                                                             risk_free_rate, volatility, 100)

    print("BINOMIAL CALL PRICE: ", round(binomial_call_value, 2))
    print("BINOMIAL PUT PRICE: ", round(binomial_put_value, 2))


if __name__ == "__main__":
    # Entry Point
    main()

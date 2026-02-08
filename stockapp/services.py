import yfinance as yf

def get_stock_data(symbol):
    """Fetches main info for a ticker using yfinance.
    Returns a dictionary of data or None if failed."""

    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")

        if history.empty:
            return None

        # yfinance returns a DataFrame; we take the last row
        latest = history.iloc[-1]
        
        # .info contains general metadata (company name, etc.)
        info = ticker.info
        """Use this print statement to sample
        what data we'd like back from yfinance.
        There is also an aapl.json file with a
        full yfinnace ticker printout"""
        # print(
        #     'symbol:', info.get('symbol', symbol),
        #     'name:', info.get('shortName', 'N/A'),
        #     'current price:', info.get('currentPrice', 'N/A'),
        #     'open:', info.get('open', 'N/A'),
        #     'close:', latest['Close']
        # )
        return {
            'symbol': symbol,
            'name': info.get('shortName', 'N/A'),
            'current_price': info.get('currentPrice', 'NA'),
            'open': info.get('open', 'NA'),
            'close': info.get('previousClose', 'AN'),
            'fifty_two_week_change': info.get('52WeekChange', 'NA'),
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None
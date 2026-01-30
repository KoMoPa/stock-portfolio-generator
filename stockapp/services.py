import yfinance as yf

def get_stock_data(symbol):
    
    #Fetches main info for a ticker using yfinance.
    #Returns a dictionary of data or None if failed.
    
    try:
        ticker = yf.Ticker(symbol)
        # .history(period="1d") gets the most recent trading day
        history = ticker.history(period="1d")

        if history.empty:
            return None

        # yfinance returns a DataFrame; we take the last row
        latest = history.iloc[-1]
        
        # .info contains general metadata (company name, etc.)
        info = ticker.info

        return {
            'symbol': symbol,
            'name': info.get('longName', 'N/A'),
            'date': latest.name.strftime('%Y-%m-%d'),
            'open_price': round(latest['Open'], 2),
            'close_price': round(latest['Close'], 2),
            'high_price': round(latest['High'], 2),
            'low_price': round(latest['Low'], 2),
            'volume': int(latest['Volume']),
            'currency': info.get('currency', 'USD'),
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None
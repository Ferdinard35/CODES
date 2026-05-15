import yfinance as yf

stock = yf.Ticker("TSLA")

print(stock.info["currentPrice"])

data = stock.history(period="1mo")
print(data)
#http://chrisdegiere.com/introduction-to-financial-market-data-visualization-with-python/

# download free end of day historical stock data
# from yahoo finance using pandas
import pandas.io.data as web
from datetime import datetime
    
end = datetime.now()
start = datetime(end.year - 5, end.month, end.day)
df = web.DataReader("SPY", 'yahoo', start, end)
     
print (df.tail())

# summary statistics accross the whole DataFrame
print ("df.describe()=\n", df.describe())

# plot the historical closing prices and volume using matplotlib
import matplotlib.pyplot as plt
plots = df[['Close', 'Volume']].plot(subplots=True, figsize=(10, 10))
plt.show()

# chart a basic 50 period moving average of the closing price
import pandas as pd
df['ma50'] = pd.rolling_mean(df['Close'], 50)
df['ma200'] = pd.rolling_mean(df['Close'], 200)
#df['ma200'] = Series.rolling(window=200, center=False).mean()
plots = df[['Close', 'ma50', 'ma200']].plot(subplots=False, figsize=(10, 4))
plt.show()
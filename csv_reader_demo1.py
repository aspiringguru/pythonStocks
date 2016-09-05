import csv
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from yahoo_finance import Share
from datetime import datetime, timedelta


#------config start------------
inputFileName = 'ASXListedCompanies.csv'
testSize = 999999999
testYahooSize = 4
histDays = 28
#------config end--------------
asxStocks = []
stockStats = []
with open(inputFileName, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    rowNum = 0
    for row in spamreader:
        if rowNum == 0:
            print ("header row")
        elif rowNum < testSize:
            #print ("type(row)=", type(row))
            #print ("row[1]=", row[1])
            asxStocks.append(row[1])
            #print(', '.join(row))
        else:
            break
        rowNum += 1
print ("len(asxStocks)=", len(asxStocks))

now = datetime.now()
print ("now=", now)
endDate = now.strftime("%Y-%m-%d")
endDateTuple = (now.year, now.month, now.day)
nowMinus = now - timedelta(days=histDays)
startDate = (nowMinus).strftime("%Y-%m-%d")
startDateTuple = (nowMinus.year, nowMinus.month, nowMinus.day)
print ("startDateTuple=", startDateTuple, " endDateTuple=", endDateTuple)
print ("startDate formatted = ", startDate, "type(startDate)=", type(startDate))
print ("endDate formatted = ", endDate, "type(endDate)=", type(endDate))

for i in range(testYahooSize):
    stockCode = asxStocks[i]+".AX"
    print ("stockCode=", stockCode)
    yahoo = Share(stockCode)
    print ("yahoo.get_open()=", yahoo.get_open())
    print ("yahoo.get_price()=", yahoo.get_price())
    print ("yahoo.get_price()=", yahoo.get_trade_datetime())
    history = yahoo.get_historical(startDate, endDate)#date format req'd different to quotes_historical_yahoo_ohlc
    print ("len(history)=", len(history))
    if len(history)>0:
        low = []
        high = []
        volume = []
        for i in range(len(history)):
            print ("history[",i,"]=", history[i], "Low=", history[i]['Low'], " type(Low)=", type(history[i]['Low']))
            temp = float(history[i]['Low'])
            low.append(temp)
            temp = float(history[i]['High'])
            high.append(temp)
            temp = int(history[i]['Volume'])
            volume.append(temp)
        print ("low=", low)
        print ("high=", high)
        print ("volume=", volume)
        minLow = min(low)
        maxHigh = max(high)
        percentChange = (maxHigh-minLow)*100/minLow #int((maxHigh-minLow)*100/minLow)/100
        print ("opened 7 days ago, ", history[0]['Open'])
        print ("over last", str(histDays), "days, min=", str(minLow), " max=", str(maxHigh), " stock ", stockCode," has changed by ", str(int(percentChange*100)/100), "%")
        stockDict = {"stockCode":stockCode, "opened":history[0]['Open'], "minLow":minLow, "maxHigh":maxHigh ,"percentChange":percentChange, "endDate": endDate}
        stockStats.append(stockDict)

print ("len(stockStats)=", len(stockStats))
maxPercentChangeUp = 0
maxPercentChangeUpPos = 0
maxPercentChangeDown = 0
maxPercentChangeDownPos = 0
for i in range(len(stockStats)):
    if stockStats[i]['percentChange']>maxPercentChangeUp:
        maxPercentChangeUp = stockStats[i]['percentChange']
        maxPercentChangeUpPos = i
    if stockStats[i]['percentChange']<maxPercentChangeDown:
        maxPercentChangeDown = stockStats[i]['percentChange']
        maxPercentChangeDownPos = i
print ("max positive stock change @ i=", maxPercentChangeUpPos, "dict = ", stockStats[maxPercentChangeUpPos])
print ("max negative stock change @ i=", maxPercentChangeDownPos, "dict = ", stockStats[maxPercentChangeDownPos])



def plotStockHist(stockCode, startDate, endDate):
    # startDate, endDate required as tuples in format (Year, month, day) to work with quotes_historical_yahoo
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12

    quotes = quotes_historical_yahoo_ohlc(stockCode, startDate, endDate)
    if len(quotes) != 0:
        #do stuff
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
        ax.xaxis.set_major_formatter(weekFormatter)
        #ax.xaxis.set_minor_formatter(dayFormatter)

        #plot_day_summary(ax, quotes, ticksize=3)
        candlestick_ohlc(ax, quotes, width=0.6)

        ax.xaxis_date()
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.ylabel('Stock Price')
        startDateStr = str(startDate[2])+"/"+str(startDate[1])+"/"+str(startDate[0])
        endDateStr = str(endDate[2])+"/"+str(endDate[1])+"/"+str(endDate[0])
        plt.xlabel("period "+startDateStr+" to "+endDateStr)
        plt.title("Stock Code:"+stockCode)
        plt.savefig("candleStickChart.png")
        #plt.show()

    else:
        #error, exit gracefully.
        print("no history found, no chart plotted.")

print ("stockStats[maxPercentChangeUpPos]['stockCode']=", stockStats[maxPercentChangeUpPos]['stockCode']
       , "startDate=", startDate, "endDate=", endDate)
print (type(stockStats[maxPercentChangeUpPos]['stockCode']), type(startDate) , type(endDate))
plotStockHist(stockStats[maxPercentChangeUpPos]['stockCode'], startDateTuple, endDateTuple)

#-------------

#-------------
import sys
import tweepy
import time
from random import randint
from keys_peterjamessmit6 import keys #keep keys in separate file, keys.py
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

# config section START - do NOT edit.
myScreenName = "peterjamessmit6" #'InspiredGuruAu'
maxTweetCharLength = 140
#minsleepTime & maxsleepTime in seconds.
#minSleepTime = 1 #reccomend min sleep time 300 seconds (5 minutes),
# 3600 seconds (30 minutes is more practical. Nobody likes a spammer
#maxSleepTime = 2 #maxSleepTime can be as large as you want.
# config section END

try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    print ("marker2")
    usersInfo = api.get_user(myScreenName)
    print ("usersInfo=", usersInfo)
    print ("type(usersInfo)=", type(usersInfo))
    print ("usersInfo.id=", usersInfo.id)
    print ("usersInfo.name=", usersInfo.name)
    print ("usersInfo.screen_name=", usersInfo.screen_name)
    print ("usersInfo.created_at=", usersInfo.created_at)
    print ("usersInfo.description=", usersInfo.description)
    print ("usersInfo.followers_count=", usersInfo.followers_count)
    print ("usersInfo._json=", usersInfo._json)
    #http://docs.tweepy.org/en/v3.5.0/api.html#API.update_with_media
    api.update_with_media(filename="candleStickChart.png", status="What do you make of this stock? #asx")
except tweepy.TweepError:
    print ("tweepy.TweepError=", tweepy.TweepError)
except Exception as e:
    print ("general exception ", e)


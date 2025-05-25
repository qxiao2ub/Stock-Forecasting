# import matplotlib.pyplot as plt
#from matplotlib.finance import candlestick2_ohlc
# from mpl_finance import candlestick2_ohlc
# import matplotlib.ticker as ticker
import quandl
import numpy as np
#import math

# refer "module_5_online_data" folder name "folder named "video_quandl_stock_prices"


# Pre-reqs:
# 1)  Install quandl:
#		pip install quandl
#        pip install mplfinance
#
# 2) Get an api key from
#		https://www.quandl.com/tools/python
#
# 3) Place the api key below:
quandl.ApiConfig.api_key = "s_Rx_BYchUddxpxxxx"

#-------1st function: importQuotes(a,b,c)-------
def importQuotes(a,b,c):
    # "YYY-MM-DD" format for dates
    '''
    # test
    ticker_symbol	= "INTC"
    date1 			= "2017-11-01"
    date2 			= "2017-11-30"
    
    '''
    ticker_symbol	= a.upper() #stock ticker, force it upper
    date1 			= b #start date
    date2 			= c #end date
    #'''
        
    # We will now use the quandl library to query for stock data.
    # `quotes` will be a numpy ndarray.
    #dataSource = "WIKI/%s" % (ticker_symbol)
    dataSource = "WIKI/%s" % (ticker_symbol)
    quotes = quandl.get(dataSource, start_date=date1, end_date=date2, returns="numpy")
    #print (quotes)
    #print (quotes.dtype) #show data type
    #print (quotes['Close'])
    return quotes['Close']

#-------2st function: forecast.forecastMA (a,b,c)-------
def forecastMA(a_ma_1,b_ma,c_ma):
    
    ma = np.average(b_ma[-a_ma_1:])    #calculate last a element of moving avg.
    ans_ma = round(ma,2)
    return ans_ma #print round up to 2 decimal of moving avg.

# '''
#-------3rd function: forecastLA (a,b)-------
def forecastLR(a_LR,b_LR):
    #a = 3 #3rd a parameter
    
    slice_cl = b_LR #all price
    #print(slice_cl)
    
    a_ma = len(slice_cl) #a_ma is total data len
    
    sum_iDi = 0
    sum_Di = 0
    
    for i in range(0,a_ma): #i = 0,1,2
        #print (i)
        #print (slice_cl[i])
        sum_iDi += (i+1)*slice_cl[i]
        sum_Di += slice_cl[i]
        
    #print("sum_idi is", sum_iDi)
    #print("sum_di is",sum_Di)
    s_xy = a_ma*sum_iDi-a_ma*(a_ma+1)/2*sum_Di
    #print("s_xy is ", s_xy)
    s_xx = a_ma*a_ma*(a_ma+1)*(2*a_ma+1)/6 - a_ma*a_ma*(a_ma+1)*(a_ma+1)/4
    #print("s_xx is ", s_xx)
    
    tot_avg = np.mean(slice_cl)
    
    b_slope = s_xy/s_xx
    #print ("b_slope is ", b_slope)
    #print ("ma is ", ma)
    a_interc = tot_avg - b_slope*(a_ma+1)/2
    #print("a_intersection is ", a_interc)
    
    t=a_LR #prediction for 1 period
    
    forecast_t = a_interc+b_slope*(t+a_ma)
    
    #print ("forecast for time period t is ", round(forecast_t,2))
    
    return (round(forecast_t,2),b_slope,a_interc)

#-------4th function: forecastHolt (a,b,c,d)-------
def forecastHolt(a_h,b_h,c_h,d_h):

# a_h = 1 #t to predict future
# b_h = 0.1 #alpha
# c_h = 0.4 #beta 
# d_h = quotes['Close'] #stock closing pricing

    all_cl = d_h
    #print("all close price is ", all_cl)
    
    a_1 = len(d_h)
    #print("length of all data:", a)
    
    sum_iDi = 0
    sum_Di = 0
    
    for i in range(0,a_1): #i = 0,1,2
        #print (i)
        #print (slice_cl[i])
        sum_iDi += (i+1)*all_cl[i]
        sum_Di += all_cl[i]
        
    #print("sum_idi is", sum_iDi)
    #print("sum_di is",sum_Di)
    s_xy_0 = a_1*sum_iDi-a_1*(a_1+1)/2*sum_Di
    #print("s_xy is ", s_xy)
    s_xx_0 = a_1*a_1*(a_1+1)*(2*a_1+1)/6 - a_1*a_1*(a_1+1)*(a_1+1)/4
    #print("s_xx is ", s_xx)
    
    tot_avg_0 = np.mean(all_cl)
    #print("4th ")
    
    b_slope_0 = s_xy_0/s_xx_0
    #print ("b_slope_0 is ", b_slope_0)
    #print ("ma is ", ma)
    a_interc_0 = tot_avg_0 - b_slope_0*(a_1+1)/2
    #print("a_intersection_0 is ", a_interc_0)
    
    s_t = [a_interc_0]
    g_t = [b_slope_0]
    
    #print(s_t[-1],g_t[-1])
     
    for j in range(0,a_1): #all s_t and g_t update
        #print(j)
        s_t_cu = b_h*all_cl[j] + (1-b_h)*(s_t[-1]+g_t[-1]) #cal current s_t
        g_t_cu = c_h*(s_t_cu-s_t[-1])+(1-c_h)*g_t[-1] #cal current g_t
        s_t.append(s_t_cu) #append current s_t to s_t list
        g_t.append(g_t_cu) #append current s_t to s_t list
    
    # print(len(s_t))
    # print(len(g_t))
    # print(len(all_cl))
    
    Holt_forecast = s_t[-1]+a_h*g_t[-1]
    return(round(Holt_forecast,2))

'''
# In this cell we are defining a function to help us format the x-axis 
#of our plot.
def mydate(x,pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''
'''

'''
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)


# Plot the time, open, high, low, close as a vertical line 
# ranging from low to high. Use a rectangular bar to 
# represent the open-close span. If close >= open, use 
# colorup to color the bar, otherwise use colordown.
candlestick2_ohlc(ax, quotes['Open'], quotes['High'], quotes['Low'], quotes['Close'], width=0.6)

xdate = quotes['Date']

ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

# Add lines connecting each day's closing price
x = []
y = []
for i in range(0, len(quotes)):
	x.append(i)
	y.append(quotes[i]['Close'])				# Closing price
plt.plot(x, y)

plt.title(ticker_symbol)

fig.autofmt_xdate()
fig.tight_layout()

plt.show()
'''

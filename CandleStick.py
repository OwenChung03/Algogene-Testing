import numpy as np
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime
df = pd.read_csv("EURUSD_Candlestick_1_D_ASK_05.05.2003-19.10.2019.csv")
df.tail()
# Check if NA values are in data
df.isna().sum()
#Engulfing pattern signals
def Revsignal1(df1):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    signal = [0] * length
    bodydiff = [0] * length

    for row in range(1, length):
        bodydiff[row] = abs(open[row]-close[row])
        bodydiffmin = 0.003
        if (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
            open[row-1]<close[row-1] and
            open[row]>close[row] and 
            #open[row]>=close[row-1] and close[row]<open[row-1]):
            (open[row]-close[row-1])>=+0e-5 and close[row]<open[row-1]):
            signal[row] = 1
        elif (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
            open[row-1]>close[row-1] and
            open[row]<close[row] and 
            #open[row]<=close[row-1] and close[row]>open[row-1]):
            (open[row]-close[row-1])<=-0e-5 and close[row]>open[row-1]):
            signal[row] = 2
        else:
            signal[row] = 0
        #signal[row]=random.choice([0, 1, 2])
        #signal[row]=1
    return signal
df['signal1'] = Revsignal1(df)
df[df['signal1']==1].count()
#Target
def mytarget(df1, barsfront):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    trendcat = [None] * length
    
    piplim = 300e-5
    for line in range (0, length-1-barsfront):
        for i in range(1,barsfront+1):
            if ((high[line+i]-max(close[line],open[line]))>piplim) and ((min(close[line],open[line])-low[line+i])>piplim):
                trendcat[line] = 3 # no trend
            elif (min(close[line],open[line])-low[line+i])>piplim:
                trendcat[line] = 1 #-1 downtrend
                break
            elif (high[line+i]-max(close[line],open[line]))>piplim:
                trendcat[line] = 2 # uptrend
                break
            else:
                trendcat[line] = 0 # no clear trend  
    return trendcat

df['Trend'] = mytarget(df,3)
conditions = [(df['Trend'] == 1) & (df['signal1'] == 1),(df['Trend'] == 2) & (df['signal1'] == 2)]
values = [1, 2]
df['result'] = np.select(conditions, values)
trendId=2
dfpl = df[400:450]
print(df[df['result']==trendId].result.count()/df[df['signal1']==trendId].signal1.count())
df[(df['Trend']!=trendId) & (df['signal1']==trendId)] # false positives
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])

fig.show()

SLTPRatio = 1.5 #TP/SL Ratio
def mytarget(barsupfront, df1):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    signal = list(df1['signal'])
    trendcat = [0] * length
    amount = [0] * length
    n1=2
    n2=2
    backCandles=45
    SL=0
    TP=0
    for line in range(backCandles, length-barsupfront-n2):
        if signal[line]==1:
            SL = max(high[line-1:line+1])#!!!!! parameters
            TP = close[line]-SLTPRatio*(SL-close[line])
            for i in range(1,barsupfront+1):
                if(low[line+i]<=TP and high[line+i]>=SL):
                    trendcat[line]=3
                    break
                elif (low[line+i]<=TP):
                    trendcat[line]=1 #win trend 1 in signal 1
                    amount[line]=close[line]-low[line+i]
                    break
                elif (high[line+i]>=SL):
                    trendcat[line]=2 #loss trend 2 in signal 1
                    amount[line]=close[line]-high[line+i]
                    break

        if signal[line]==2:
            SL = min(low[line-1:line+1])#!!!!! parameters
            TP = close[line]+SLTPRatio*(close[line]-SL)
    
            for i in range(1,barsupfront+1):
                if(high[line+i]>=TP and low[line+i]<=SL):
                    trendcat[line]=3
                    break
                elif (high[line+i]>=TP):
                    trendcat[line]=2 #win trend 2 in signal 2
                    amount[line]=high[line+i]-close[line]
                    break
                elif (low[line+i]<=SL):
                    trendcat[line]=1 #loss trend 1 in signal 2
                    amount[line]=low[line+i]-close[line]
                    break
    #return trendcat
    return amount

df['Trend'] = mytarget(16, df)
df['Amount'] = mytarget(16, df)

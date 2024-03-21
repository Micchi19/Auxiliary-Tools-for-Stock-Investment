# from pandas_datareader import data
import yfinance as yf
import pandas as pd
import csv
from flag import *
from get_ma import *
yf.pdr_override()

golden_cross_checker = []

for i in range(1300, 10001):
    code_i = str(i) + ".T"
    try:
        data_60m = yf.download(code_i, period="30d", interval="30m") # DataFrameに株価情報を格納(60足)
        data_1d  = yf.download(code_i, period="1d", interval="1d")   # DataFrameに株価情報を格納(日足)
        
        # 直近の日出来高が100,000以上の株式のみ抽出対象とする
        if(data_1d.loc[:,"Volume"].iloc[-1] > 100000): # if not data_1d.empty:
            candlestick_60m_25 = data_60m.loc[:,"Close"].iloc[-25:]         # 5足移動平均線算出 (5MA) のための25本のローソク足 ( 5 + 20日分)(60分足)
            candlestick_60m_45 = data_60m.loc[:,"Close"].iloc[-45:]         # 25足移動平均線算出(25MA)のための45本のローソク足 (25 + 20日分)(60分足)
            candlestick_1d_45  = data_1d.loc[:,"Close"].iloc[-45:]          # 25足移動平均線算出(25MA)のための45本のローソク足 (25 + 20日分)(日足)
            row_25 = candlestick_60m_25.shape[0]                            # row_25 = 25    
            
            # 5MAの算出
            moving_average_60m_5  = get_ma_5(candlestick_60m_25)            # (60分足)
            # 25MAの算出
            moving_average_60m_25 = get_ma_25(candlestick_60m_45)           # (60分足)
            moving_average_1d_25  = get_ma_25(candlestick_1d_45)             # (日足)

            # 条件
            if(term5(moving_average_1d_25) and term6(moving_average_60m_5, moving_average_60m_25)):
                golden_cross_checker.append(code_i)
        else:
            print(f"Skipping {code_i}: No data available")
    except Exception as e:
        print(f"Skipping {code_i}: {e}")

print(golden_cross_checker)

writer_golden_cross_checker = [[item] for item in golden_cross_checker if item != "\n"]
with open("Result/code.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(writer_golden_cross_checker)

# # 株式情報を取得
# ticker_info = yf.Ticker("***.T")
# # 会社概要(info)を出力
# ticker_info.info
# # 株価データ（日毎）を取得
# hist = ticker_info.history(period="max")
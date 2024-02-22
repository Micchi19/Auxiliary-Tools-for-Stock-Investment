# from pandas_datareader import data
import yfinance as yf
import pandas as pd
import csv
from flag import *
yf.pdr_override()


# df = data.get_data_yahoo("9984.T", "2022-1-5", "2023-9-13")

# for code_i in code:
#     try:
#         df_60m = data.get_data_yahoo(code_i, period="200d", interval="60m") # DataFrameに株価情報を格納
#         if not data.empty:
#             print(f"it's empty")
#     except Exception as e:
#         print(f"Skipping {code}: {e}")

golden_cross_checker = []

for i in range(9000, 10001): # for i in range(1300, 10001):
    code_i = str(i) + ".T"
    try:
        data_60m = yf.download(code_i, period="30d", interval="60m") # DataFrameに株価情報を格納
        data_1d = yf.download(code_i, period="1d", interval="1d")   # DataFrameに株価情報を格納
        if not data_60m.empty:
            candlestick_25 = data_60m.loc[:,"Close"].iloc[-25:]                 # 5足移動平均線算出 (5MA) のための25本のローソク足 (5  + 20日分)
            candlestick_45 = data_60m.loc[:,"Close"].iloc[-45:]                 # 25足移動平均線算出(25MA)のための45本のローソク足 (25 + 20日分)
            row_25 = candlestick_25.shape[0]                         # row_25 = 25
            moving_average5 = []                                     # 5MA (60分足)
            moving_average25 = []                                    # 25MA(60分足)
            
            if(data_1d.loc[:,"Volume"].iloc[-2] > 100000):                      # 直近の日出来高が100,000以上の株式のみ抽出対象とする
                # 5MAの算出
                for i in range(20):
                    tmp = 0
                    for j in range(5):
                        tmp += candlestick_25.iloc[i + j]
                    tmp /= 5
                    moving_average5.append(tmp)
                moving_average5.reverse()                            # 1要素目が直近のMAの値

                # 25MAの算出
                for i in range(20):
                    tmp = 0
                    for j in range(25):
                        tmp += candlestick_45.iloc[i + j]
                    tmp /= 25
                    moving_average25.append(tmp)
                moving_average25.reverse()                           # 1要素目が直近のMAの値

                # 条件1 && 条件2 && 条件3 && 条件4
                if(term_1(moving_average5, moving_average25) and term_2(moving_average5, candlestick_25, row_25) and \
                   term_3(moving_average25, moving_average5, data_60m) and term_4(moving_average25, moving_average5)):
                    golden_cross_checker.append(code_i) 
        else:
            print(f"Skipping {code_i}: No data available")
    except Exception as e:
        print(f"Skipping {code_i}: {e}")

print(golden_cross_checker)

writer_golden_cross_checker = [[item] for item in golden_cross_checker if item != "\n"]
with open("Stock/Result/code.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(writer_golden_cross_checker)

# df_1d = data.get_data_yahoo("7974.T", period="200d", interval="1d")

# # 株式情報を取得
# ticker_info = yf.Ticker("***.T")
# # 会社概要(info)を出力
# ticker_info.info
# # 株価データ（日毎）を取得
# hist = ticker_info.history(period="max")
    

list_today = []
list_all = []

with open("Stock/Result/result.csv") as f:
    reader = f.read() # reader: str型

# reader = list(filter(lambda x: x != "\n", reader)) # 空白文字を削除

# 空白文字によってリストに分割(各要素は1日分の株価が「,」で連続している状態)
list_previous = reader.split("\n")
list_previous = list_previous[:-1]

for item in list_previous:
    list_tmp = item.split(",")
    list_all.append(list_tmp)

# for item_all in list_all:
#     for i in item_all:
#         i = float(i)


for code_i in golden_cross_checker:
    data_60m = yf.download(code_i, period="1d", interval="60m") # DataFrameに株価情報を格納
    if not data_60m.empty:
        list_data_60m = [item for item in data_60m.loc[:,"Close"]]
        list_today.append(list_data_60m)

print(list_today)

if len(list_all) == 0:
    list_all = list_today
else:
    for index, row in enumerate(list_all):
        row += list_today[index]

# for item_all in list_all:
#     for i in item_all:
#         i = float(i)

with open("/Stock/Result/result.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(list_all)
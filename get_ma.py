def get_ma_5(candlestick):                      # 条件 : 25要素以上のローソク足
    moving_average = []
    for i in range(20):
        tmp = 0
        for j in range(5):
            tmp += candlestick.iloc[i + j]
        tmp /= 5
        moving_average.append(tmp)
    moving_average.reverse()                    # 1要素目が直近のMAの値
    return moving_average                       # 20要素分のMA

def get_ma_25(candlestick):                     # 条件 : 45要素以上のローソク足
    moving_average = []
    for i in range(20):
        tmp = 0
        for j in range(25):
            tmp += candlestick.iloc[i + j]
        tmp /= 25
        moving_average.append(tmp)
    moving_average.reverse()                    # 1要素目が直近のMAの値
    return moving_average                       # 20要素分のMA
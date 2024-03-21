# 増えていくと思う
# 条件1     過去5時間(60分*5)の5MA が 25MA より下
def term1(moving_average5, moving_average25):
    flag_1st = True
    for i in range(5):
        if(moving_average5[i] > moving_average25[i]):
            flag_1st = False
    return flag_1st

# 条件2     過去5時間(60分*5)の計5本のローソク足の内、4本以上が5MA(60分足)を超えている　（過去5時間の需要の勢いを調査）
def term2(moving_average5, candlestick_25, row_25):
    cnt = 0
    for i in range(5):
        cnt = cnt + \
            1 if(moving_average5[i] < candlestick_25.iloc[row_25 - i - 1]) else cnt
    flag_2nd = True
    if(cnt < 4):
        flag_2nd = False
    return flag_2nd

# 条件3     直近の5MA(60分足)と25MA(60分足)との差が 現在の株価の0.5% 以内
def term3(moving_average25, moving_average5, data_60m):
    flag_3rd = ((moving_average25[0] - moving_average5[0]) \
                 < (data_60m.loc[:,"Close"].iloc[-1] / 200))
    return flag_3rd

# 条件4     5足分の5MAと25MAにある程度大きな乖離がある
#           ただ、乖離を定量的に表現する方法が分かっていない
#           現在の株価との比率で表そうとしても企業によってボラリティが異なるため、エントリーしやすい形を見逃す可能性大
#           株価に応じてパターン分けすべきか？（100~999円までなら○○%以上、1000~5000円までなら××%以上なら乖離、みたいな）
#           ただボラリティの大小は株価じゃなくてセクターとかによって変わるのかな？それとも各企業特有の特徴なのか？
#           後者だとすると、判別するの難しいな
def term4(moving_average25, moving_average5):
    min_price = moving_average25[0] - moving_average5[0]
    for i in range(18): # 3日分
        min_price = moving_average25[i] - moving_average5[i] if min_price > (moving_average25[i] - moving_average5[i]) else min_price
    if(min_price != (moving_average25[0] - moving_average5[0]) or (moving_average25[17] - moving_average5[17])):
        flag_4th = True
    else:
        flag_4th = False
    return flag_4th

# 条件5     過去5日分の25MA が 上向き
def term5(moving_average25):
    flag_5th = True
    for i in range(5):
        if(moving_average25[i] - moving_average25[i + 1] > 0):
            flag_5th = False
    return flag_5th

# 条件6     5MA < 25MA  -> 条件4 && 条件5 であれば反発が予想される？
def term6(moving_average5, moving_average25):
    flag_6th = True
    if(moving_average5[0] > moving_average25[0]):
        flag_6th = False
    return flag_6th
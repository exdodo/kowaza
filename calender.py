#%%
import pandas as pd
import h5py
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import calendar
def holiday_list() :
    '''
    休日リストの取得　
    ネットがだめな場合保存先から
    '''    
    japanese_holiday_url = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
    try :
        df = pd.read_csv(japanese_holiday_url, encoding="SHIFT_JIS")
        df.to_csv('holiday_bk.csv',encoding="SHIFT_JIS")
    except :
        print('url読込エラー')
        df=pd.read_csv('holiday_bk.csv', encoding="SHIFT_JIS")
    holyday_ls=[i for i in df['国民の祝日・休日月日']]    
    return holyday_ls

def output_calendar(salesday_ls=[],dtToday=datetime.datetime.today()):    
    # 祝日、日曜日、土曜日の色を指定
    color_code = {
        "honjitu":"",
        "salesday":"\033[41m""\033[1m",
        "holiday": "\033[91m",
        "sunday": "\033[91m",
        "saturday": "\033[94m",
        "end": "\033[0m"
    }
    # 週の始まりの曜日を指定
    calendar.setfirstweekday(calendar.SUNDAY)

    # 現在の年月を取得
    year = dtToday.year
    month = dtToday.month

    # 日付を週ごとのリストにして変数に代入
    days = calendar.monthcalendar(year, month)

    # カレンダーを出力
    output = " {}年 {}月\n".format(str(year), str(month))
    output += " Su Mo Tu We Th Fr Sa\n"
    #休日リスト　string
    holyday_ls=holiday_list()   
    
    for line in days:
        for i in range(7):
            str_day = str(line[i]).rjust(3)
            
            # 値が0の場合空欄にする
            if line[i] == 0:
                output += "   "
            # 読込営業日を色分け
            elif datetime.date(year, month, line[i]) in salesday_ls :
                output += color_code["salesday"] + str_day + color_code["end"]
            # 祝日を判定し色分け
            elif str(year)+'/'+str(month)+'/'+ str(line[i]) in holyday_ls :
                output += color_code["holiday"] + str_day + color_code["end"]

            # 日曜日の場合色分け
            elif i == 0:
                output += color_code["sunday"] + str_day + color_code["end"]

            # 土曜日の場合色分け
            elif i == 6:
                output += color_code["saturday"] + str_day + color_code["end"]

            else:
                output += str_day

        output += "\n"
    return output
def calende_print(month_num=2) :    
    for  i in reversed(range(0,month_num)) :
        print(output_calendar([],
            (datetime.datetime.today() - relativedelta(months=i)))
            ,end="")
'''
def calender_hyouji(scode='n0101',month_num=2):
    df_ns=load_data('hdf',scode) #hdf yahoo fred quandl
    df_days = df_ns.copy()
    #df_days['week'] = df_ns.index.strftime('%a')
    df_days['weekday'] = df_ns.index.weekday    
    #営業読み込み日を2ヶ月表示
    salesday_ls=[(i.to_pydatetime()).date() for i in df_days.index]
    for  i in reversed(range(0,month_num)) :
        print(output_calendar(salesday_ls,
            (datetime.datetime.today() - relativedelta(months=i)))
            ,end="")
'''
if __name__ == '__main__':
    calende_print(month_num=5)    
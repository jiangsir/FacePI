import pandas as pd
import os

basepath = os.path.dirname(os.path.realpath(__file__))

def test():
    csvfile = 'address.csv'
    df = pd.read_csv(csvfile)
    print(type(df))
    print(df.tail()) ## 查看 data frame 的前幾筆資料
    new_row = ['aa','bb','cc', 'cc', 'dd']
    ss = pd.Series(new_row, index=df.columns, name='e')
    df = df.append(ss)
    new_row = ['aaa','bbb','ccc', 'ddd', 'eee']
    ss = pd.Series(new_row, index=df.columns, name='e')
    df = df.append(ss)
    df.tail() ## 查看 data frame 的前幾筆資料
    df.to_csv(csvfile,index=False,sep=',')

def addSignin(name, personid, confidence, textconfidence, timestamp):
    csvfile = os.path.join(basepath, "Signin_log.csv")
    df = pd.read_csv(csvfile)
    new_row = [name, personid, confidence, textconfidence, timestamp]
    ss = pd.Series(new_row, index=df.columns, name='e')
    df = df.append(ss)
    df.to_csv(csvfile,index=False,sep=',')

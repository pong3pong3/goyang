import pandas as pd
import numpy as np
goyang = pd.read_csv('goyang.csv',encoding='cp949', thousands=',')
goyang['주소'] = goyang['주소'].astype(str).apply(lambda x: x.strip()[8:])
goyang.loc[781,'주소']+='동'
goyang['날짜']=goyang['날짜'].astype(str).apply(lambda x: x.strip())
nan=goyang[goyang['날짜'].str.startswith('20')==False].index
for i in nan:
    j=i-1
    while j in nan:
        j-=1
    goyang.loc[i,'날짜']=goyang.loc[j,'날짜']
old=goyang[(goyang['날짜'].str.startswith('2020')|goyang['날짜'].str.startswith('2019'))==False].index
goyang.loc[old[:1],'날짜']='2019'
goyang.loc[old[1:],'날짜']='2020'
goyang.columns = list(goyang.columns)[:-1]+['허가']
goyang.loc[pd.isna(goyang['허가']), '허가'] = 0
#goyang['면적']=goyang['면적'].astype(str).str.replace(',','').astype(np.float64())
goyang['구']=goyang['주소'].apply(lambda x: x.split(' ')[0])
goyang['동']=goyang['주소'].apply(lambda x: x.split(' ')[-1])
goyang['연도']=goyang['날짜'].apply(lambda x: x[2:4])
goyang.drop(columns=['주소','날짜']).to_csv('gy_tidy.csv',index=False)


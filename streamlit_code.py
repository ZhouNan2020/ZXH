import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy as cp
import time
#%%


#%%
# 这一段不要动，我特么目前还没有搞太明白谷歌的API怎么工作的
# 目前可以知道的是：scopes是范围，但是地址就是这个而不是sheet的链接
scopes = ["https://spreadsheets.google.com/feeds"]
# 为特定的账户开设key，然后然后把账户给到谷歌sheet的访问权限中，通过key访问这个账户关联的sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)
#这个json就是key，授权给谷歌的表格
client = gspread.authorize(credentials)
# 这一段就牛逼了，这一段那串乱码是目标谷歌sheet地址中间那一部分，用.来确定要访问的工作表
global sheet
sheet = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1

#%%
#下面的就可以动了

tab1, tab2, tab3 = st.tabs(["日常喂养记录", "特殊情况记录", "数据分析"])

with tab1:
        timeticks = time.time()
        date=time.strftime("%Y-%m-%d", time.localtime())
        time=time.strftime("%H:%M:%S", time.localtime())
        Breastfeeding = st.number_input('母乳亲喂（单位:分钟）')
        BreastBottleFeeding = st.number_input('母乳瓶喂（单位:ml）')
        FormulaMilkPowder = st.number_input('配方奶粉（单位:ml）')

        Shit = st.checkbox('大便')
        Shit_value = 0
        if Shit:
                Shit_value = 1

        Pee = st.checkbox('小便')
        Pee_value = 0
        if Pee:
                Pee_value = 1
            
        ChangeDiapers = st.checkbox('换尿布')
        ChangeDiapers_value = 0
        if ChangeDiapers:
                ChangeDiapers_value = 1
        record = [timeticks,date,time, Breastfeeding, BreastBottleFeeding, FormulaMilkPowder,Shit_value,Pee_value,ChangeDiapers_value]
        if st.button('提交本次记录'):
                sheet.append_row(record,1)
                st.success('提交成功')



class MeanAnalysis:
            def __init__(self, num):
                    date = sheet.col_values(2)[1:]
                    date = pd.DataFrame(date)
                    date.columns = ['date']
                    value_all = sheet.col_values(num)[1:]
                    value_all = pd.DataFrame(value_all)
                    value_all.columns = ['value_all']
                    value_all = value_all.astype('float')
                    sheet_all = pd.concat([date, value_all], axis=1)
                    sheet_all.drop(index=0, axis=0, inplace=True)
                    sheet_nozero = sheet_all.drop(sheet_all[sheet_all['value_all'] == 0].index)
                    st.write(sheet_nozero)
                    mean_all = sheet_all.groupby('date').mean()
            def tail_15(self):
                    mead_tail_15 = self.mean_all.tail(15)
                    return mead_tail_15
            def tail_7(self):
                    mead_tail_7 = self.mean_all.tail(7)
                    return mead_tail_7
            def tail_3(self):
                    mead_tail_3 = self.mean_all.tail(3)
                    return mead_tail_3
            def tail_1(self):
                    mead_tail_1 = self.mean_all.tail(1)
                    return mead_tail_1




with tab3:
        date = sheet.col_values(2)[1:]
        date = pd.DataFrame(date)
        date.columns = ['date']
        st.write(date)
        value_all = sheet.col_values(4)[1:]
        value_all = pd.DataFrame(value_all)
        value_all.columns = ['value_all']
        st.write(value_all)
        sheet_all = pd.concat([date, value_all], axis=1)
        sheet_all.drop(index=0, axis=0, inplace=True)
        st.write(sheet_all)
        # st.write(sheet_all)
        # mean_all = sheet_all.groupby('date').mean()









# append_row这个是谷歌的方法，可以直接在sheet中添加一行数据
#tes=("hjj","king")
#sheet.append_row(tes,1)

#sheet = pd.DataFrame(sheet.get_all_records())

#st.write(sheet)

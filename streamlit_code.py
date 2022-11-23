import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy as cp
import time
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib as mpl
import datetime
#%%
font = font_manager.FontProperties(fname='simhei.ttf')
parameters = {'xtick.labelsize': 16,
              'ytick.labelsize': 16,
              'axes.unicode_minus':False}
plt.rcParams.update(parameters)
plt.style.use('ggplot')

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
global sheet1
sheet1 = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1
sheet2 = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('工作表2')

#%%
#下面的就可以动了

tab1, tab2, tab3,tab4 = st.tabs(["日常喂养记录", "特殊情况记录", "数据分析","覃薇吸奶记录"])




with tab1:

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

        if st.button('提交本次记录'):
                timeticks1 = time.time()
                date1 = time.strftime("%Y-%m-%d", time.localtime())
                time1 = time.strftime("%H:%M:%S", time.localtime())
                record = [timeticks1, date1, time1, Breastfeeding, BreastBottleFeeding, FormulaMilkPowder, Shit_value,
                          Pee_value, ChangeDiapers_value]
                sheet1.append_row(record, 1)
                st.success('提交成功')



class MeanAnalysis:
            def __init__(self, num,name):
                    date = sheet1.col_values(2)[1:]
                    date = pd.DataFrame(date)
                    date.columns = ['date']
                    value_all = sheet1.col_values(num)[1:]
                    value_all = pd.DataFrame(value_all)
                    value_all.columns = [str(name)]
                    value_all = value_all.astype('int')
                    sheet_all = pd.concat([date, value_all], axis=1)
                    sheet_all.drop(index=0, axis=0, inplace=True)
                    sheet_nozero = sheet_all.drop(sheet_all[sheet_all[str(name)] == 0].index)
                    mean_all = sheet_nozero.groupby('date').mean()
                    self.mean_all = mean_all
            def tail(self,tail_num):
                    mean_tail = self.mean_all.tail(tail_num)
                    mean_tail = mean_tail.astype('int')
                    return mean_tail





with tab3:
        st.subheader('数据分析')
        daynum = st.slider('想分析周栩珩最近多少天的状态？', 1, 15, 3)
        if st.button('开始分析'):
                name1 = '近{}日每日平均母乳亲喂时间'.format(daynum)
                mean_breastfeeding = MeanAnalysis(4,name1)
                mean_breastfeeding=mean_breastfeeding.tail(daynum)
                fig, ax = plt.subplots()
                ax.plot(mean_breastfeeding.index, mean_breastfeeding[str(name1)], 'o-')
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                ax.set_ylabel('亲喂时长', fontsize=16, fontproperties=font)
                ax.set_title(str(name1), fontsize=16, fontproperties=font)
                st.pyplot(fig)


def count_milk():
        date = sheet1.col_values(2)[1:]
        date = pd.DataFrame(date)
        date.columns = ['date']
        count = sheet2.col_values(4)[1:]
        count = pd.DataFrame(count)
        count.columns = ['count']
        count = count.astype('int')
        all_count = pd.concat([date, count], axis=1)
        day_count = all_count.groupby('date').sum()
        return day_count


with tab4:
        st.subheader('覃薇吸奶记录')
        col1, col2= st.columns(2)
        with col1:
                if st.button('记录一次吸奶'):
                        timeticks2 = time.time()
                        date2 = time.strftime("%Y-%m-%d", time.localtime())
                        time2 = time.strftime("%H:%M:%S", time.localtime())
                        sheet2.append_row([timeticks2,date2,time2,1], 1)
                        st.success('记录成功')
        with col2:
                milkdate = sheet2.col_values(2)[-1:]
                milktime = sheet2.col_values(3)[-1:]
                st.write('上次吸奶时间：',milkdate[0],milktime[0])
                day_count = count_milk()
                fig, ax = plt.subplots()
                ax.plot(day_count.index, day_count['count'], 'o-')
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                ax.set_ylabel('吸奶次数', fontsize=16, fontproperties=font)
                st.pyplot(fig)












# append_row这个是谷歌的方法，可以直接在sheet中添加一行数据
#tes=("hjj","king")
#sheet1.append_row(tes,1)

#sheet1 = pd.DataFrame(sheet1.get_all_records())

#st.write(sheet1)

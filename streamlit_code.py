import pandas as pd
import pytz
import streamlit as st
import gspread
from matplotlib.ticker import MultipleLocator
from oauth2client.service_account import ServiceAccountCredentials
import copy as cp
import time
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib as mpl
import datetime
#%%
st.title('周栩珩成长日记')
font = font_manager.FontProperties(fname='simhei.ttf')
plt.rcParams['font.family']=['SimHei']
parameters = {'xtick.labelsize': 16,
              'ytick.labelsize': 16,
              'axes.unicode_minus':False}
plt.rcParams.update(parameters)
plt.style.use('ggplot')

#%%
# 这一段不要动，我特么目前还没有搞太明白谷歌的API怎么工作的
# 目前可以知道的是：scopes是范围，但是地址就是这个而不是sheet的链接
#@st.cache(ttl=300)
def connect_to_google_sheet():
        scopes = ["https://spreadsheets.google.com/feeds"]
# 为特定的账户开设key，然后然后把账户给到谷歌sheet的访问权限中，通过key访问这个账户关联的sheet
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)
#这个json就是key，授权给谷歌的表格
        client = gspread.authorize(credentials)
# 这一段就牛逼了，这一段那串乱码是目标谷歌sheet地址中间那一部分，用.来确定要访问的工作表
        sheet_A = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1
        sheet_B = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('工作表2')
        sheet_C = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('工作表3')
        sheet_D = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('特殊记录')
        sheet_E = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('屎尿吃药表')
        return sheet_A, sheet_B, sheet_C, sheet_D, sheet_E


#%%
#下面的就可以动了
tab1, tab2, tab3,tab4 = st.tabs(["日常喂养记录", "特殊情况记录", "数据分析","覃薇吸奶记录"])
timeticks = time.time()
date = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")
time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%H:%M:%S")
global sheet1, sheet2, sheet3, sheet4
sheet1, sheet2, sheet3, sheet4,sheet5 = connect_to_google_sheet()


st.cache(ttl=600)
class he_we:
    def __init__(self):
            dataframe = pd.DataFrame(sheet3.get_all_records())
            self.dataframe = dataframe.tail(10)
    def plot(self):
            dataframe = pd.DataFrame(self.dataframe)
            dataframe = dataframe.set_index('date')
            x = dataframe.index
            y1 = dataframe['height']
            y2 = dataframe['weight']
            return x, y1, y2

with st.sidebar:
        st.header('身高体重记录')
        height_weight = he_we()
        x, y1, y2 = height_weight.plot()
        fig, ax1 = plt.subplots()
        ax1.plot(x, y1, color='red', label='身高', marker='o')
        ax1.set_xlabel('日期', fontproperties=font)
        plt.xticks(rotation=45)
        ax1.set_ylabel('身高', fontproperties=font)
        ax1.tick_params(axis='y', labelcolor='red')
        ax1.legend(loc='best', prop=font)
        ax2 = ax1.twinx()
        ax2.plot(x, y2, color='blue', label='体重', marker='o')
        ax2.set_ylabel('体重', fontproperties=font)
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.legend(loc='best', prop=font)
        #for a, b in zip(list(x), list(y1)):
                #ax1.text(a, b + 1, b, ha='center', va='bottom', fontsize=10)
        #for a, c in zip(list(x), list(y2)):
                #ax2.text(a, c + 1, c, ha='center', va='bottom', fontsize=10)
        st.pyplot(fig)
        height_value = st.number_input('身高(cm)', value=0.0, step=0.1)
        weight_value= st.number_input('体重(kg)', value=0.0, step=0.1)
        if height_value ==0.00:
                height=y1.tolist()[-1]
        else:
                height = height_value
        if weight_value ==0.00:
                weight=y2.tolist()[-1]
        else:
                weight = weight_value
        if st.button('提交', key='submit_2'):
                sheet3.append_row([date, height, weight])
                st.success('提交成功')


@st.cache(ttl=60)
class today:
    def __init__(self):
        eattabel = pd.DataFrame(sheet1.get_all_records())
        self.tail = eattabel.iloc[-1:]
        shittable = pd.DataFrame(sheet5.get_all_records())
        all_sum = shittable.groupby('date').sum()
        today = all_sum.iloc[-1:]
        self.today = today
    def lasteverything(self, name):
        return self.tail[name].values[0]
    def todayeverything(self, name):
        return self.today[name].values[0]


with tab1:
        today = today()
        st.write('上一次喂养：{}，母乳亲喂{}分钟，母乳瓶喂{}ml，奶粉{}ml'.format(today.lasteverything('time'), today.lasteverything('Breastfeeding'), today.lasteverything('BreastBottleFeeding'), today.lasteverything('FormulaMilkPowder')))
        st.subheader('本次记录↓↓↓')
        Breastfeeding = st.number_input('母乳亲喂（单位:分钟）',value=0,step=1)
        BreastBottleFeeding = st.number_input('母乳瓶喂（单位:ml）',value=0,step=1)
        FormulaMilkPowder = st.number_input('配方奶粉（单位:ml）',value=0,step=1)

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
        Mamiai = st.checkbox('妈咪爱')
        Mamiai_value = 0
        if Mamiai:
                Mamiai_value = 1
        ADconsole = st.checkbox('AD滴丸')
        ADconsole_value = 0
        if ADconsole:
                ADconsole_value = 1

        if st.button('提交本次记录',key='submit_1'):
                record = [timeticks, date, time, Breastfeeding, BreastBottleFeeding, FormulaMilkPowder, Shit_value,
                          Pee_value, ChangeDiapers_value, Mamiai_value, ADconsole_value]
                sheet1.append_row(record, 1)
                st.success('提交成功')
                today = today()
                st.write('今日喂养总量: ',today.todayeverything('Breastfeeding')+today.todayeverything('BreastBottleFeeding')+today.todayeverything('FormulaMilkPowder'))
                st.write('母乳亲喂{}分钟 '.format(today.todayeverything('Breastfeeding')))
                st.write('母乳瓶喂{}毫升 '.format(today.todayeverything('BreastBottleFeeding')))
                st.write('配方奶粉{}毫升 '.format(today.todayeverything('FormulaMilkPowder')))
                st.write('今日已拉粑粑{}次，已换尿布{}次，已服用妈咪爱{}次，已服用AD滴丸{}次'.format(today.todayeverything('Shit'), today.todayeverything('ChangeDiapers'), today.todayeverything('Mamiai'), today.todayeverything('ADconsole')))



class Analysis:
            def __init__(self):
                    datafrmae = pd.DataFrame(sheet1.get_all_records())
                    self.datafrmae = datafrmae
            def day_mean(self,tail_num,name):
                    data_nozero = self.datafrmae.drop(self.datafrmae[self.datafrmae[str(name)] == 0].index)
                    data_nozero.set_index('date', inplace=True)
                    data_nozero = data_nozero[str(name)]
                    median = data_nozero.median()
                    max = data_nozero.max()
                    min = data_nozero.min()
                    mean_all = data_nozero.groupby('date').mean()
                    mean_tail = mean_all.tail(tail_num)
                    mean_tail = mean_tail.astype('int')
                    return mean_tail,median,max,min
            def day_sum(self,tail_num,name):
                    sum_all = self.datafrmae.groupby('date').sum()
                    sum_all = sum_all[str(name)]
                    median = sum_all.median()
                    max = sum_all.max()
                    min = sum_all.min()
                    sum_tail = sum_all.tail(tail_num)
                    sum_tail = sum_tail.astype('int')
                    return sum_tail,median,max,min
            def shit_ticks(self,tail_num,name):
                    datafrmae = self.datafrmae
                    dataframe = pd.DataFrame(datafrmae.drop(self.datafrmae[self.datafrmae[str(name)] == 1].index))
                    dataframe = pd.concat([dataframe['date'], dataframe['ticks']], axis=1)
                    dataframe.set_index('date', inplace=True)
                    dataframe = dataframe.diff(axis=0, periods=1)
                    dataframe = dataframe.groupby('date').mean()
                    dataframe = dataframe.astype('int')
                    dataframe = dataframe / 60
                    dataframe = round(dataframe, 2)
                    return dataframe


class temper_metric:
        def __init__(self):
                datafrmae = pd.DataFrame(sheet4.get_all_records())
                self.datafrmae = datafrmae
        def temper(self):
                datafrmae = pd.DataFrame(self.datafrmae)
                datafrmae = datafrmae.set_index('time')
                today = datafrmae[datafrmae['date']==date]
                datafrmae = datafrmae['temper']
                datafrmae = datafrmae.astype('float')
                current = datafrmae.values[-1]
                last = datafrmae.values[-2]
                delta = current-last
                delta = round(delta,2)
                return delta,today


with tab2:
        st.write('该版面会依据周栩珩当前需要记录的特殊情况调整')
        st.subheader('目前仅开放记录体温和大便颜色')
        st.subheader('1.体温')
        temper=st.number_input('本次体温',step=0.1,min_value=35.0,max_value=42.0)
        if st.button('提交本次体温记录',key='temper'):
                sheet4.append_row([timeticks,date,time,temper],1)
        temp = temper_metric()
        delta = temp.temper()[0]
        st.metric(label="目前体温", value=temper, delta=delta,delta_color="inverse")
        temp_plot = pd.DataFrame(temp.temper()[1])
        fig, ax = plt.subplots()
        ax.plot(temp_plot.index, temp_plot['temper'])
        ax.set_xlabel('时间',fontproperties=font,fontsize=12)
        ax.set_ylabel('体温',fontproperties=font,fontsize=12)
        ax.set_title('本日体温曲线',fontproperties=font,fontsize=12)
        st.pyplot(fig)
        st.subheader('2.大便颜色')

with tab3:
        st.subheader('数据分析')
        daynum = st.slider('想分析周栩珩最近多少天的状态？', 1, 15, 3)

        if st.button('开始分析'):
                ana = Analysis()
                name1 = '近{}日每日平均母乳亲喂时间'.format(daynum)
                mean_breastfeeding=pd.DataFrame(ana.day_mean(daynum,'Breastfeeding')[0])
                fig, ax = plt.subplots()
                ax.plot(mean_breastfeeding.index, mean_breastfeeding['Breastfeeding'], 'o-')
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                ax.set_ylabel('日均亲喂时间', fontsize=16, fontproperties=font)
                ax.set_title(str(name1), fontsize=16, fontproperties=font)
                #for a, b in zip(list(mean_breastfeeding.index), list(mean_breastfeeding['Breastfeeding'])):
                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
                st.pyplot(fig)

                name2 = '近{}日每日平均喂养量'.format(daynum)
                mean_bottle=pd.DataFrame(ana.day_mean(daynum,'BreastBottleFeeding')[0])
                mean_formulamilkpowder = pd.DataFrame(ana.day_mean(daynum, 'FormulaMilkPowder')[0])
                fig, ax = plt.subplots()
                ax.plot(mean_bottle.index, mean_bottle['BreastBottleFeeding'], 'o-')
                ax.plot(mean_formulamilkpowder.index, mean_formulamilkpowder['FormulaMilkPowder'], 's-')
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                plt.legend(['母乳瓶喂', '配方奶粉'], loc='upper left', prop=font)
                ax.set_ylabel('喂养量', fontsize=16, fontproperties=font)
                ax.set_title(str(name2), fontsize=16, fontproperties=font)
                #for a, b in zip(list(mean_bottle.index), list(mean_bottle['BreastBottleFeeding'])):
                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
                #for a, b in zip(list(mean_formulamilkpowder.index), list(mean_formulamilkpowder['FormulaMilkPowder'])):
                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
                st.pyplot(fig)
                median = ana.day_mean(daynum,'BreastBottleFeeding')[1]
                max = ana.day_mean(daynum,'BreastBottleFeeding')[2]
                min = ana.day_mean(daynum,'BreastBottleFeeding')[3]
                st.write('近{}日母乳瓶喂量中位数为{}毫升，最大值为{}毫升，最小值为{}毫升'.format(daynum,median,max,min))
                median = ana.day_mean(daynum,'FormulaMilkPowder')[1]
                max = ana.day_mean(daynum,'FormulaMilkPowder')[2]
                min = ana.day_mean(daynum,'FormulaMilkPowder')[3]
                st.write('近{}日配方奶粉喂量中位数为{}毫升，最大值为{}毫升，最小值为{}毫升'.format(daynum,median,max,min))

                name3 = '近{}日每日拉屎次数'.format(daynum)
                shit_sum = pd.DataFrame(ana.day_sum(daynum,'Shit')[0])
                fig, ax = plt.subplots()
                ax.bar(x=shit_sum.index,height=shit_sum['Shit'],width=0.5,align='center',color='steelblue',alpha=0.8,edgecolor='black')
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                ax.set_ylabel('拉屎次数', fontsize=16, fontproperties=font)
                ax.set_title(str(name3), fontsize=16, fontproperties=font)
                #for a, b in zip(list(shit_sum.index),list(shit_sum['Shit'])):
                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
                st.pyplot(fig)
                median = ana.day_sum(daynum,'Shit')[1]
                max = ana.day_sum(daynum,'Shit')[2]
                min = ana.day_sum(daynum,'Shit')[3]
                st.write('近{}日拉屎次数中位数为{}次，最大值为{}次，最小值为{}次'.format(daynum,median,max,min))

                name4 = '近{}日每日平均拉屎间隔时间'.format(daynum)
                shit_day = pd.DataFrame(ana.shit_ticks(daynum,'Shit'))
                fig, ax = plt.subplots()
                ax.bar(shit_day.index, shit_day['ticks'], width=0.5, align='center', color='steelblue', alpha=0.8)
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                ax.set_ylabel('平均拉屎间隔时间（分钟）', fontsize=16, fontproperties=font)
                ax.set_title(str(name4), fontsize=16, fontproperties=font)
                #for a, b in zip(list(shit_day.index),list(shit_day['ticks'])):
                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
                st.pyplot(fig)


#@st.cache(ttl=600)
class suctionOfMilk:
        def __init__(self):
                self.datafrmae = pd.DataFrame(sheet2.get_all_records())

        def lastSuckingTime(self):
                data = self.datafrmae
                data = data['time']
                data = (data.tail(1)).values[0]
                return data
        def lastMilkML(self):
                data = self.datafrmae
                data = data['Quantity']
                data = data.tail(1).values[0]
                return data
        def dailyMilkIntake(self):
                data = self.datafrmae
                data = data.set_index('date')
                data = data['count']
                data = data.groupby('date').sum()
                data = data.tail(7)
                return data
        def dailyMilkMl(self):
                data = self.datafrmae
                data = data.set_index('date')
                data = data['Quantity']
                data = data.groupby('date').mean()
                data = data.tail(7)
                return data


with tab4:
        st.subheader('覃薇吸奶记录')
        col1, col2= st.columns([1,2])
        suc = suctionOfMilk()

        with col1:
                suctionVolume = st.number_input('吸出量（单位:ml）')
                dailytimes = pd.DataFrame(suc.dailyMilkIntake())
                dailymilk = pd.DataFrame(suc.dailyMilkMl())
                if st.button('记录本次吸奶'):
                        sheet2.append_row([timeticks,date,time,suctionVolume,1], 1)
                        st.success('记录成功')
        with col2:
                st.write('最近一次吸奶时间：', str(suc.lastSuckingTime()))
                st.write('最近一次吸奶量：', str(suc.lastMilkML()))
                fig, ax = plt.subplots()
                ax1 = ax.twinx()
                ax.plot(dailytimes.index, dailytimes['count'], 'o-')
                ax1.bar(dailymilk.index, dailymilk['Quantity'], width=0.5, alpha=0.5)
                ax.set_ylabel('日吸奶次数', fontsize=16, fontproperties=font)
                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
                ax1.set_ylabel('日均吸奶量', fontsize=16, fontproperties=font)
                plt.xticks(rotation=45)
                #for a, c in zip(list(dailymilk.index), list(dailymilk['Quantity'])):
                        #plt.text(a, c + 2, c, ha='center', va='center', fontsize=14)
                ax.legend(['日吸奶次数'], loc='upper left', prop=font)
                ax1.legend(['日均吸奶量'], loc='upper right', prop=font)
                st.pyplot(fig)



























# append_row这个是谷歌的方法，可以直接在sheet中添加一行数据
#tes=("hjj","king")
#sheet1.append_row(tes,1)

#sheet1 = pd.DataFrame(sheet1.get_all_records())

#st.write(sheet1)

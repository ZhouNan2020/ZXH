
import pandas as pd
import pytz
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import matplotlib.pyplot as plt
from matplotlib import font_manager
import datetime
#%%
class today_eatable:
    def __init__(self):

        eattabel = pd.DataFrame(sheet1.get_all_records())
        self.table = eattabel
        self.tail = eattabel.iloc[-1:]
        all_sum = eattabel.groupby('date').sum()
        self.all_sum = all_sum
        today = all_sum.iloc[-1:]
        self.today = today
    def lasteverything(self, name):
        return self.tail[name].values[0]
    def todayeverything(self, name):
        return self.today[name].values[0]
    def last_day_eat(self,name):
        day = self.all_sum.iloc[-1:]
        day = day[name].values[0]
        return day
    def select_day_everything(self, name, day):
        day = self.all_sum.iloc[-day:-day+1]
        day = day[name].values[0]
        return day
    def lastcoltime(self, name):
        coltable = pd.DataFrame(self.table.drop(self.table[self.table[name] == 0].index))
        coltable = coltable.iloc[-1:]
        time=coltable['time'].values[0]
        return time
    def show(self):
        table = pd.DataFrame(self.table)
        table = table.iloc[:,2:6]
        table = table.set_index('time')
        table.rename(columns={'Breastfeeding':'母乳亲喂（分钟）','BreastBottleFeeding':'母乳瓶喂（ml）','FormulaMilkPowder':'配方奶粉（ml）'},inplace=True)
        #table.style.highlight_min()
        #table.replace(0, '没吃', inplace=True)
        return table.tail(10)
    def averageFeedingAmount(self):
        table = pd.DataFrame(self.table)
        table = table.iloc[:,4:6]
        table_sum = table.iloc[:,0:2].sum(axis=1)
        table_sum = table_sum.to_frame()
        table_sum_nozero = table_sum.drop(table_sum[table_sum[0] == 0].index)
        table_sum_tail = table_sum_nozero.tail(50)
        table_sum_tail_mean = table_sum_tail.mean()
        table_sum_tail_mean = table_sum_tail_mean.values[0]
        table_sum_tail_mean = round(table_sum_tail_mean,2)
        return table_sum_tail_mean
    def judg_formula(self):
        value = self.today['FormulaMilkPowder'].values[0]
        if value == 0:
            st.error('今天还没有吃配方奶粉')
        else:
            st.success('今天已经吃了配方奶粉')





class today_shittable:
    def __init__(self):

        shittable = pd.DataFrame(sheet5.get_all_records())
        self.table = shittable
        self.tail = shittable.iloc[-1:]
        all_sum = shittable.groupby('date').sum()
        today = all_sum.iloc[-1:]
        self.today = today
    def lasteverything(self, name):
        return self.tail[name].values[0]
    def todayeverything(self, name):
        return self.today[name].values[0]
    def lastcoltime(self, name):
        coltable = pd.DataFrame(self.table.drop(self.table[self.table[name] == 0].index))
        coltable = coltable.iloc[-1:]
        time=coltable['time'].values[0]
        return time
    def show(self):
        table = pd.DataFrame(self.table)
        table = table.iloc[:,2:8]
        table = table.set_index('time')
        table.rename(columns={'Shit':'屎','Pee':'尿','ChangeDiapers':'换尿布','Mamiai':'益生菌','ADconsole':'AD滴丸'},inplace=True)
        #table.replace(1,'有',inplace=True)
        return table.tail(10)
    def judg_AD(self):
        value = self.today['ADconsole'].values[0]
        if value == 0:
            st.error('今天还没有吃AD滴丸')
        else:
            st.success('今天已经吃了AD滴丸')

    def judg_shit(self):
        value = self.today['Shit'].values[0]
        if value == 1:
            st.warning('今天只拉了一次大便噢')
        else:
            pass

    def judg_mamiai(self):
        value = self.today['Mamiai'].values[0]
        if value == 0:
            st.error('今天还没有吃益生菌')
        else:
            st.success('今天已经吃了益生菌')
    def judg_temper(self):
        table = self.table
        today = pd.DataFrame(self.table.drop(self.table[self.table['date'] !=date].index))
        today_temper = pd.DataFrame(today.drop(today[today['temper']==0].index))
        temper_count = len(today_temper)
        if temper_count ==0:
            st.error('今天还没有测体温')
        elif temper_count <5:
            st.warning('今天测体温不足5次')
        elif temper_count >=5 and temper_count <10:
            st.info('今天测体温已经达到5次')
        elif temper_count >=10:
            st.success('今天的体温监测很密集')



class Analysis:
    def __init__(self):
        data_eat = pd.DataFrame(sheet1.get_all_records())
        data_shit = pd.DataFrame(sheet5.get_all_records())
        self.datafrmae_eat = data_eat
        self.datafrmae_shit = data_shit

    def day_mean(self, name,tail_num=7):
        data_nozero = self.datafrmae_eat.drop(self.datafrmae_eat[self.datafrmae_eat[str(name)] == 0].index)
        data_nozero.set_index('date', inplace=True)
        data_nozero = data_nozero[str(name)]
        median = data_nozero.median()
        max = data_nozero.max()
        min = data_nozero.min()
        mean_all = data_nozero.groupby('date').mean()
        mean_tail = mean_all.tail(tail_num)
        mean_tail = mean_tail.astype('int')
        return mean_tail, median, max, min



#%%
st.info('点击屏幕左上角右拉→箭头，查看今日待办事项')
st.markdown('---')
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
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").worksheet('屎尿吃药表')

        return sheet_A,sheet_B



#%%
#下面的就可以动了

tab1, tab2 = st.tabs(["喂养状态总览","新增记录",])
timeticks = time.time()
global date,time_value,time_auto
date = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")
time_value = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
time_auto = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%H:%M:%S")
#st.write(time_value.strftime("%H"))

sheet1,sheet5 = connect_to_google_sheet()

#@st.cache(ttl=60)
#class he_we:
#    def __init__(self):
#            sheet5 = connect_to_google_sheet()[2]
#            dataframe = pd.DataFrame(sheet3.get_all_records())
#            self.dataframe = dataframe.tail(10)
#            self.sheet3 = sheet3
#    def show(self):
#            dataframe = pd.DataFrame(self.dataframe)
#            dataframe = dataframe.set_index('date')
#            dataframe.rename(columns={'height':'身高','weight':'体重',},inplace=True)
#            return dataframe
#    def append(self, date, height, weight):
#            self.sheet3.append_row([date, height, weight])
#
#
#with st.sidebar:
#
#        st.header('身高体重记录')
#        height_value = st.number_input('身高(cm)', value=0.0, step=0.1)
#        weight_value= st.number_input('体重(kg)', value=0.0, step=0.1)
#        if st.button('提交', key='submit_2'):
#                sheet3 = connect_to_google_sheet()[2]
#                sheet3.append(date, height_value, weight_value)
#                st.success('提交成功')
#        if st.button('显示身高体重记录',key = 'height_weight'):
#                hw = he_we()
#                hewe = hw.show()
#                st.write(hewe)




#@st.cache(ttl=60)
with st.sidebar:

    today_eat = today_eatable()
    today_shit = today_shittable()
    today_shit.judg_AD()
    today_shit.judg_mamiai()
    today_eat.judg_formula()
    today_shit.judg_shit()
    today_shit.judg_temper()






with tab1:
        today_eat = today_eatable()
        today_shit = today_shittable()

        st.subheader('上一次喂养：{}'.format(today_eat.lasteverything('time')))
        st.markdown('**喂养内容：**')
        st.markdown('1.母乳亲喂**{}**分钟'.format(today_eat.lasteverything('Breastfeeding')))
        st.markdown('2.母乳瓶喂**{}**ml'.format(today_eat.lasteverything('BreastBottleFeeding')))
        st.markdown('3.奶粉**{}**ml'.format(today_eat.lasteverything('FormulaMilkPowder')))


        st.markdown('-------')
        def show_last_time():
            lasttime = today_eat.lasteverything('time')
            lasttime = datetime.datetime.strptime(lasttime, "%H:%M:%S")
            nexteatTime = (lasttime + datetime.timedelta(minutes=150)).strftime("%H:%M:%S")
            warmtime1 = (lasttime + datetime.timedelta(minutes=110)).strftime("%H:%M:%S")
            warmtime2 = (lasttime + datetime.timedelta(minutes=130)).strftime("%H:%M:%S")
            return nexteatTime, warmtime1, warmtime2
        st.markdown('**下一次喂养**')
        st.markdown('下一次喂养时间可能在**{}**左右'.format(show_last_time()[0]))
        st.markdown('可以在**{}**到**{}**温奶'.format(show_last_time()[1],show_last_time()[2]))
        st.markdown('如果下一次准备瓶喂的话，根据最近**50**次的瓶喂量（母乳+奶粉）均值，下一次热奶的量至少要有**{}**ml'.format((today_eat.averageFeedingAmount())))

        st.markdown('-------')
        st.subheader('今日喂养总览：')
        st.write('母乳亲喂{}分钟'.format(today_eat.todayeverything('Breastfeeding')))
        st.write('母乳瓶喂{}ml'.format(today_eat.todayeverything('BreastBottleFeeding')))
        st.write('奶粉{}ml'.format(today_eat.todayeverything('FormulaMilkPowder')))
        st.write('今日总计：共{}分钟亲喂+{}ml瓶喂（母乳或奶粉）'.format(today_eat.todayeverything('Breastfeeding'),
                                          today_eat.todayeverything('BreastBottleFeeding')+today_eat.todayeverything('FormulaMilkPowder')))

        st.markdown('--------')
        day=st.slider('滑动圆点选择关注过去几天的喂养情况', min_value=2, max_value=10,step=1,value=3)
        st.caption('注意：如果选择2，那么就是昨天的喂养情况，选择3，就是前天的喂养情况，以此类推')
        if st.button('显示过去喂养情况',key='show_eat'):

                st.write('母乳亲喂{}分钟'.format(today_eat.select_day_everything('Breastfeeding',day=day)))
                st.write('母乳瓶喂{}ml'.format(today_eat.select_day_everything('BreastBottleFeeding',day=day)))
                st.write('奶粉{}ml'.format(today_eat.select_day_everything('FormulaMilkPowder',day=day)))
                st.write('总计：共{}分钟亲喂+{}ml瓶喂（母乳或奶粉）'.format(today_eat.select_day_everything('Breastfeeding',day=day),
                                                  today_eat.select_day_everything('BreastBottleFeeding',day=day)+today_eat.select_day_everything('FormulaMilkPowder',day=day)))
        st.markdown('-------')
        st.markdown('**今日杂项：**')
        st.write('上一次大便：{}'.format(today_shit.lastcoltime('Shit')))
        st.write('今日大便次数：{}次'.format(today_shit.todayeverything('Shit')))
        st.write('今日服用益生菌：{}次'.format(today_shit.todayeverything('Mamiai')))
        st.write('今日服用AD滴丸：{}次'.format(today_shit.todayeverything('ADconsole')))
        st.markdown('-------')
        st.subheader('近期喂养总览')
        st.markdown('**最近10次喂养记录：**')
        st.table(today_eat.show())
        st.markdown('**最近10次屎尿吃药记录：**')
        st.table(today_shit.show())
        analysis = Analysis()
        st.markdown('**最近7天日均母乳瓶喂量：**')
        fig,ax = plt.subplots()
        ax.plot(analysis.day_mean('BreastBottleFeeding')[0])
        plt.xticks(rotation=45)
        st.pyplot(fig)




def time_input(key_number):
    time_number = st.text_input('手动输入时间（如果不输入则自动记录当前时间）',value='',key=key_number)
    if time_number != '':
        time_format = datetime.datetime.strptime(str(time_number), '%H.%M')
        time = time_format.strftime('%H:%M:%S')
    else:
        time = time_auto
    return time



with tab2:
        st.subheader('喂养记录')


        Breastfeeding = st.number_input('母乳亲喂（单位:分钟）',value=0,step=1)
        BreastBottleFeeding = st.number_input('母乳瓶喂（单位:ml）',value=0,step=1)
        FormulaMilkPowder = st.number_input('配方奶粉（单位:ml）',value=0,step=1)
        time_1 = time_input(key_number=1)
        st.caption('格式示例：八点四十五，输入的格式为：8.45，使用小数点代替时间中间的冒号')


        if st.button('提交喂养记录',key='feed'):
                #sheet1 = connect_to_google_sheet()[0]
                sheet1.append_row([timeticks, date,time_1,Breastfeeding,BreastBottleFeeding,FormulaMilkPowder],1)
                st.success('喂养记录已提交')



        st.markdown('---')


        st.subheader('屎尿吃药记录')

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
        Mamiai = st.checkbox('益生菌')
        Mamiai_value = 0
        if Mamiai:
                Mamiai_value = 1
        ADconsole = st.checkbox('AD滴丸')
        ADconsole_value = 0
        if ADconsole:
                ADconsole_value = 1
        time_2 = time_input(key_number=2)
        st.caption('格式示例：八点四十五，输入的格式为：8.45，使用小数点代替时间中间的冒号')


        if st.button('提交屎尿吃药记录',key='shit'):
                #sheet5 = connect_to_google_sheet()[1]
                record_2 = [timeticks, date, time_2, Shit_value,Pee_value, ChangeDiapers_value, Mamiai_value, ADconsole_value,0]
                sheet5.append_row(record_2, 1)
                st.success('屎尿吃药记录已提交')






            #def day_mean(self,tail_num,name):
            #        data_nozero = self.datafrmae.drop(self.datafrmae[self.datafrmae[str(name)] == 0].index)
            #        data_nozero.set_index('date', inplace=True)
            #        data_nozero = data_nozero[str(name)]
            #        median = data_nozero.median()
            #        max = data_nozero.max()
            #        min = data_nozero.min()
            #        mean_all = data_nozero.groupby('date').mean()
            #        mean_tail = mean_all.tail(tail_num)
            #        mean_tail = mean_tail.astype('int')
            #        return mean_tail,median,max,min
            #def day_sum(self,tail_num,name):
            #        sum_all = self.datafrmae.groupby('date').sum()
            #        sum_all = sum_all[str(name)]
            #        median = sum_all.median()
            #        max = sum_all.max()
            #        min = sum_all.min()
            #        sum_tail = sum_all.tail(tail_num)
            #        sum_tail = sum_tail.astype('int')
            #        return sum_tail,median,max,min
            #def shit_ticks(self,tail_num,name):
            #        datafrmae = self.datafrmae
            #        dataframe = pd.DataFrame(datafrmae.drop(self.datafrmae[self.datafrmae[str(name)] == 0].index))
            #        dataframe = pd.concat([dataframe['date'], dataframe['ticks']], axis=1)
            #        dataframe.set_index('date', inplace=True)
            #        dataframe = dataframe.diff(axis=0, periods=1)
            #        dataframe = dataframe.groupby('date').mean()
            #        dataframe = dataframe.astype('int')
            #        dataframe = dataframe / 60
            #        dataframe = round(dataframe, 2)
            #        return dataframe
            #

class temper_metric:
        def __init__(self):
                datafrmae = pd.DataFrame(sheet5.get_all_records())
                self.datafrmae = datafrmae
        def temper(self):
                datafrmae = pd.DataFrame(self.datafrmae)
                datafrmae = datafrmae.set_index('time')
                datafrmae = datafrmae.drop(datafrmae[datafrmae['temper'] == 0].index)
                last10 = datafrmae.tail(10)
                last10 = last10['temper']
                last10 = last10.astype('float')
                current = last10.values[-1]
                last = last10.values[-2]
                delta = current-last
                delta = round(delta,2)
                return delta,last10,current





#with tab4:
#        st.subheader('数据分析')
#        daynum = st.slider('想分析周栩珩最近多少天的状态？', 1, 15, 3)
#
#        if st.button('开始分析'):
#                ana = Analysis()
#                name1 = '近{}日每日平均母乳亲喂时间'.format(daynum)
#                mean_breastfeeding=pd.DataFrame(ana.day_mean(daynum,'Breastfeeding')[0])
#                fig, ax = plt.subplots()
#                ax.plot(mean_breastfeeding.index, mean_breastfeeding['Breastfeeding'], 'o-')
#                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
#                plt.xticks(rotation=45)
#                ax.set_ylabel('日均亲喂时间', fontsize=16, fontproperties=font)
#                ax.set_title(str(name1), fontsize=16, fontproperties=font)
#                #for a, b in zip(list(mean_breastfeeding.index), list(mean_breastfeeding['Breastfeeding'])):
#                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
#                st.pyplot(fig)
#
#                name2 = '近{}日每日平均喂养量'.format(daynum)
#                mean_bottle=pd.DataFrame(ana.day_mean(daynum,'BreastBottleFeeding')[0])
#                mean_formulamilkpowder = pd.DataFrame(ana.day_mean(daynum, 'FormulaMilkPowder')[0])
#                fig, ax = plt.subplots()
#                ax.plot(mean_bottle.index, mean_bottle['BreastBottleFeeding'], 'o-')
#                ax.plot(mean_formulamilkpowder.index, mean_formulamilkpowder['FormulaMilkPowder'], 's-')
#                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
#                plt.xticks(rotation=45)
#                plt.legend(['母乳瓶喂', '配方奶粉'], loc='upper left', prop=font)
#                ax.set_ylabel('喂养量', fontsize=16, fontproperties=font)
#                ax.set_title(str(name2), fontsize=16, fontproperties=font)
#                #for a, b in zip(list(mean_bottle.index), list(mean_bottle['BreastBottleFeeding'])):
#                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
#                #for a, b in zip(list(mean_formulamilkpowder.index), list(mean_formulamilkpowder['FormulaMilkPowder'])):
#                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
#                st.pyplot(fig)
#                median = ana.day_mean(daynum,'BreastBottleFeeding')[1]
#                max = ana.day_mean(daynum,'BreastBottleFeeding')[2]
#                min = ana.day_mean(daynum,'BreastBottleFeeding')[3]
#                st.write('近{}日母乳瓶喂量中位数为{}毫升，最大值为{}毫升，最小值为{}毫升'.format(daynum,median,max,min))
#                median = ana.day_mean(daynum,'FormulaMilkPowder')[1]
#                max = ana.day_mean(daynum,'FormulaMilkPowder')[2]
#                min = ana.day_mean(daynum,'FormulaMilkPowder')[3]
#                st.write('近{}日配方奶粉喂量中位数为{}毫升，最大值为{}毫升，最小值为{}毫升'.format(daynum,median,max,min))
#
#                name3 = '近{}日每日拉屎次数'.format(daynum)
#                shit_sum = pd.DataFrame(ana.day_sum(daynum,'Shit')[0])
#                fig, ax = plt.subplots()
#                ax.bar(x=shit_sum.index,height=shit_sum['Shit'],width=0.5,align='center',color='steelblue',alpha=0.8,edgecolor='black')
#                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
#                plt.xticks(rotation=45)
#                ax.set_ylabel('拉屎次数', fontsize=16, fontproperties=font)
#                ax.set_title(str(name3), fontsize=16, fontproperties=font)
#                #for a, b in zip(list(shit_sum.index),list(shit_sum['Shit'])):
#                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
#                st.pyplot(fig)
#                median = ana.day_sum(daynum,'Shit')[1]
#                max = ana.day_sum(daynum,'Shit')[2]
#                min = ana.day_sum(daynum,'Shit')[3]
#                st.write('近{}日拉屎次数中位数为{}次，最大值为{}次，最小值为{}次'.format(daynum,median,max,min))
#
#                name4 = '近{}日每日平均拉屎间隔时间'.format(daynum)
#                shit_day = pd.DataFrame(ana.shit_ticks(daynum,'Shit'))
#                fig, ax = plt.subplots()
#                ax.bar(shit_day.index, shit_day['ticks'], width=0.5, align='center', color='steelblue', alpha=0.8)
#                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
#                plt.xticks(rotation=45)
#                ax.set_ylabel('平均拉屎间隔时间（分钟）', fontsize=16, fontproperties=font)
#                ax.set_title(str(name4), fontsize=16, fontproperties=font)
#                #for a, b in zip(list(shit_day.index),list(shit_day['ticks'])):
#                        #plt.text(a, b + 2, b, ha='center', va='center', fontsize=14)
#                st.pyplot(fig)


#@st.cache(ttl=600)
#class suctionOfMilk:
#        def __init__(self):
#                self.datafrmae = pd.DataFrame(sheet2.get_all_records())
#
#        def lastSuckingTime(self):
#                data = self.datafrmae
#                data = data['time']
#                data = (data.tail(1)).values[0]
#                return data
#        def lastMilkML(self):
#                data = self.datafrmae
#                data = data['Quantity']
#                data = data.tail(1).values[0]
#                return data
#        def dailyMilkIntake(self):
#                data = self.datafrmae
#                data = data.set_index('date')
#                data = data['count']
#                data = data.groupby('date').sum()
#                data = data.tail(7)
#                return data
#        def dailyMilkMl(self):
#                data = self.datafrmae
#                data = data.set_index('date')
#                data = data['Quantity']
#                data = data.groupby('date').mean()
#                data = data.tail(7)
#                return data
#
#
#with tab5:
#        st.subheader('覃薇吸奶记录')
#        col1, col2= st.columns([1,2])
#        suc = suctionOfMilk()
#
#        with col1:
#                suctionVolume = st.number_input('吸出量（单位:ml）')
#                dailytimes = pd.DataFrame(suc.dailyMilkIntake())
#                dailymilk = pd.DataFrame(suc.dailyMilkMl())
#                if st.button('记录本次吸奶'):
#                        sheet2.append_row([timeticks,date,time,suctionVolume,1], 1)
#                        st.success('记录成功')
#        with col2:
#                st.write('最近一次吸奶时间：', str(suc.lastSuckingTime()))
#                st.write('最近一次吸奶量：', str(suc.lastMilkML()))
#                fig, ax = plt.subplots()
#                ax1 = ax.twinx()
#                ax.plot(dailytimes.index, dailytimes['count'], 'o-')
#                ax1.bar(dailymilk.index, dailymilk['Quantity'], width=0.5, alpha=0.5)
#                ax.set_ylabel('日吸奶次数', fontsize=16, fontproperties=font)
#                ax.set_xlabel('日期', fontsize=16, fontproperties=font)
#                ax1.set_ylabel('日均吸奶量', fontsize=16, fontproperties=font)
#                plt.xticks(rotation=45)
#                #for a, c in zip(list(dailymilk.index), list(dailymilk['Quantity'])):
#                        #plt.text(a, c + 2, c, ha='center', va='center', fontsize=14)
#                ax.legend(['日吸奶次数'], loc='upper left', prop=font)
#                ax1.legend(['日均吸奶量'], loc='upper right', prop=font)
#                st.pyplot(fig)






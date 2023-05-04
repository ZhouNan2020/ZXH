# 二项分布
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
            

        

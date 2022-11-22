import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy as cp
#%%
from gsheetsdb import connect

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
sheet = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1
#%%
#下面的就可以动了
# append_row这个是谷歌的方法，可以直接在sheet中添加一行数据
tes=("hjj","king")
sheet.append_row(tes,1)

sheet = pd.DataFrame(sheet.get_all_records())

st.write(sheet)

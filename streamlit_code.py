import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy as cp
#%%
from gsheetsdb import connect

#%%

scopes = ["https://spreadsheets.google.com/feeds"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)

client = gspread.authorize(credentials)

sheet = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1
tes=("hjj","king")
sheet.append_row(tes,1)

sheet = pd.DataFrame(sheet.get_all_records())

st.write(sheet)

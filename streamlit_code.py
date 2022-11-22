import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#%%
from gsheetsdb import connect

#%%

scopes = ["https://docs.google.com/spreadsheets/d/16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM/edit?usp=sharing"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)

client = gspread.authorize(credentials)

sheet = client.open_by_key(
        "16cvjJKBqGoFjOxrDgdLGYzZgkffnFFOkBfhW7ra1DsM").sheet1


st.write(sheet.get_all_records())

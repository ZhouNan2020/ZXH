import streamlit as st
#%%
from gsheetsdb import connect

#%%
# Create a connection object.
conn = connect()
#%%
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows
test1="hg"
test2="hut"
sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
run_query(f'INSERT INTO "{sheet_url}" (test1,test2) VALUES ("{test1}","{test2}")')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")
import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

SHEET_ID = "1keGmcj7H6nv4-30ldgRJk0byZcCElGj1vomQeczveXM"
GID = "1011196788"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
df = pd.read_csv(url, skiprows=4)
df = df.rename(columns={df.columns[1]: "姓名"})

weekday_index = datetime.datetime.today().weekday()
weekday_map = ["星期一", "星期二", "星期三", "星期四", "星期五"]
if weekday_index >= 5:
    st.warning("今天是週末，沒有復健課程")
else:
    today_col = weekday_map[weekday_index]
    st.title(f"📅 今日復健課程表（{today_col}）")
    today_schedule = df[["姓名", today_col]].dropna()
    today_schedule = today_schedule[today_schedule[today_col] != ""]

    def parse_time(t):
        try:
            return datetime.datetime.strptime(str(t).strip(), "%H:%M").time()
        except:
            return None

    today_schedule["排序時間"] = today_schedule[today_col].apply(parse_time)
    today_schedule = today_schedule.sort_values(by="排序時間", na_position="last")

    for _, row in today_schedule.iterrows():
        st.write(f"🕒 {row[today_col]} - 👤 {row['姓名']}")

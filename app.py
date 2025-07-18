import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 連線到 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# 設定 Google Sheet 的網址與 GID
SHEET_ID = "1keGmcj7H6nv4-30ldgRJk0byZcCElGj1vomQeczveXM"
GID = "1011196788"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
st.write("https://docs.google.com/spreadsheets/d/1keGmcj7H6nv4-30ldgRJk0byZcCElGj1vomQeczveXM/edit?gid=1011196788#gid=1011196788")
st.write(url)

# 讀取資料
df = pd.read_csv(url, skiprows=3)
df = df.rename(columns={df.columns[1]: "姓名"})

# 計算今天是星期幾
weekday_index = datetime.datetime.today().weekday()
weekday_map = ["星期一", "星期二", "星期三", "星期四", "星期五"]
if weekday_index >= 5:
    st.warning("今天是週末，沒有復健課程")
    st.stop()

today = weekday_map[weekday_index]
st.title(f"📅 今日復健課程表（{today}）")

# 篩選今天上課的學生資料
time_columns = df.columns[6:]  # 從第 7 欄開始都是時間欄（例如 08:30、09:00...）
today_schedule = df[["姓名", today] + list(time_columns)]

# 建立時段對應表：時間 ➜ [(姓名, 課程種類)]
schedule_by_time = {}

for _, row in today_schedule.iterrows():
    name = row["姓名"]
    course_type = row[today]

    for time in time_columns:
        value = row[time]
        if pd.notna(value):
            schedule_by_time.setdefault(time, []).append((name, course_type))

# 顯示時段排程
for time in sorted(schedule_by_time.keys()):
    st.subheader(f"⏰ {time}")
    for name, course_type in schedule_by_time[time]:
        st.markdown(f"- 👤 {name}｜{course_type}")

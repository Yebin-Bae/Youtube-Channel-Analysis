import pandas as pd
import sqlite3

df = pd.read_excel("metadata.xlsx")  

conn = sqlite3.connect("metadata.db")

df.to_sql("youtube_videos", conn, if_exists="replace", index=False)

conn.close()
print("db file successfully transformed.")
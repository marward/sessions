import pandas as pd
from string import ascii_uppercase
from io import StringIO


text = """index,customer_id,timestamp
74594,1,2016-05-25 15:39:41
74556,1,2016-05-25 15:40:33
74403,1,2016-05-25 15:43:26
73783,1,2016-05-25 15:52:40
73241,1,2016-05-25 16:01:01
71960,1,2016-05-25 16:19:35
71590,1,2016-05-25 16:26:05
11765,2,2016-05-25 18:03:18
81825,3,2016-05-25 13:14:55
81560,3,2016-05-25 13:22:15
80517,3,2016-05-25 13:27:36
78370,3,2016-05-25 13:30:58
75575,3,2016-05-25 15:22:00
74890,3,2016-05-25 15:33:56
74119,3,2016-05-25 15:47:57"""

iter_str = StringIO(text)
print(iter_str)
df = pd.read_csv(iter_str)

df.timestamp = pd.to_datetime(df.timestamp)

def split_user(data, first_session):
    switch = data.timestamp.diff() > pd.Timedelta(minutes=3)
    session_id = switch.cumsum()
    n_sessions = session_id.nunique()
    data["session_id"] = session_id.map(
        pd.Series(
            list(
                range(first_session, first_session + n_sessions)
            )
        )
    )
    return data, n_sessions


first_session = 0
result = []
for _, data in df.groupby("customer_id"):
    splited_user, n_sessions_use = split_user(data, first_session)
    first_session += n_sessions_use
    result.append(splited_user)
    
df = pd.concat(result)

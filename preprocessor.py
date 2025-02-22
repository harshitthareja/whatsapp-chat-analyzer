import re
import pandas as pd

def preprocess(data):
    # Define regex patterns for 24-hour and 12-hour (AM/PM) time formats
    pattern_24hr = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern_12hr = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\s*-\s'

    # Detect time format in the input data
    if re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)', data, re.IGNORECASE):
        pattern = pattern_12hr
        am_pm_format = True
    else:
        pattern = pattern_24hr
        am_pm_format = False

    # Extract messages and timestamps
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean and convert the 'message_date' column
    df['message_date'] = df['message_date'].str.replace('\u202F', ' ', regex=True).str.strip()

    if am_pm_format:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce')
    else:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')

    # Drop invalid date entries
    df = df.dropna(subset=['message_date']).reset_index(drop=True)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message content
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract date components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Generate period column
    df['period'] = df['hour'].apply(lambda h: f"{h:02d}-{(h+1)%24:02d}")

    return df

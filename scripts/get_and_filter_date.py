import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent.parent
input_csv = script_dir / 'processed_csvs' / 'unfiltered_output.csv'
output_csv = script_dir / 'processed_csvs' / 'cumulative_messages.csv'

df = pd.read_csv(input_csv)

# extract username from author column
# regex: () - the group. [^'] - match any character EXCEPT a single quote. * match zero or more occurences
df['author'] = df['author'].str.extract("'username': '([^']*)'")[0]

# convert timestamp to datetime and filter out invalid timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')

# remove invalid timestamps and missing usernames
df = df.dropna(subset=['timestamp', 'author'])

# filter dates: Sep 2023 - Sep 2025
start_date = "2023-09-01"
end_date = "2025-09-30"

df = df[
    (df['timestamp'] >= start_date) & 
    (df['timestamp'] <= end_date)
    ]

# extract month and year
df['months'] = df['timestamp'].dt.to_period('M')

# count messages per user per month
monthly_counts = df.pivot_table(index='author',
                                columns='months',
                                values='timestamp',
                                aggfunc='count',
                                fill_value=0)

# ensure every month is represented
all_months = pd.period_range(start=start_date, end=end_date, freq='M')

monthly_counts = monthly_counts.reindex(columns=all_months, fill_value=0)

# calculate cumulative message counts
cumulative_counts = monthly_counts.cumsum(axis=1)

# format column names for Flourish
cumulative_counts.columns = cumulative_counts.columns.strftime('%b %Y')

# reset author index
cumulative_counts = cumulative_counts.reset_index()

# export CSV
cumulative_counts.to_csv(output_csv, index=False)

print(f'Saved cumulative dates message counts to: {output_csv}')
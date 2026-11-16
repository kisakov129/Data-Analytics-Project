import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent.parent / 'processed_csvs'
input_csv = script_dir / 'unfiltered_output.csv'
output_csv = script_dir / 'mentions.csv'

df = pd.read_csv(input_csv)

# regex: () - the group. [^'] - match any character EXCEPT a single quote. * match zero or more occurences
df['mentions'] = df['mentions'].str.findall(r"'username': '([^']*)'")

# keep rows where mentions is not empty
df = df[df['mentions'].str.len() > 0]

# explode the mentions column so that each mention gets its own row
df = df.explode('mentions')

df = df[['mentions']]

# save updated CSV
df.to_csv(output_csv, index=False)

print(f'Saved updated CSV with mentions only to: {output_csv}')
import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent.parent / 'processed_csvs'
input_csv = script_dir / 'unfiltered_output.csv'
output_csv = script_dir / 'messages.csv'

df = pd.read_csv(input_csv)

df = df[['content']].rename(columns={'content': 'messages'})

# save updated CSV
df.to_csv(output_csv, index=False)

print(f'Saved updated CSV with messages only to: {output_csv}')
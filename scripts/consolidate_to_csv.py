import pandas as pd
import os
from pathlib import Path

script_dir = Path(__file__).parent.parent
source_JSON = script_dir / 'general_messages'
output_path = script_dir / 'processed_csvs' / 'unfiltered_output.csv'

# list to hold all the dataframes
dfs = []

# consolidate all JSON files into a single CSV
for file in os.listdir(source_JSON):
    filepath = os.path.join(source_JSON, file)
    print(f'Reading: {filepath}')

    try:
        df = pd.read_json(filepath)
        dfs.append(df)
    except Exception as e:
        print(f'Failed to read {file}: {e}')

# merge all dataframes
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(output_path, index=False)
    print(f'Merged and saved to {output_path}')
else:
    print('No data to merge.')
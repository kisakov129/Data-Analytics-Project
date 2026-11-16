import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

input_csv = Path(__file__).parent.parent / 'processed_csvs' / 'mentions.csv'
output_csv = Path(__file__).parent.parent / 'word_clouds' / 'usernames_wordcloud.png'

df = pd.read_csv(input_csv)

# extract usernames from mentions column
all_usernames = df['mentions'].tolist()

# get the frequency of each username
username_counts = Counter(all_usernames)

# remove deleted user from the word cloud
username_counts.pop('Deleted User', None)

wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
).generate_from_frequencies(username_counts)

# display the word cloud
plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud.to_file(output_csv)
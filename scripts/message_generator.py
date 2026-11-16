import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from pathlib import Path

input_csv = Path(__file__).parent.parent / 'processed_csvs' / 'messages.csv'
output_csv = Path(__file__).parent.parent / 'word_clouds' / 'messages_wordcloud.png'

df = pd.read_csv(input_csv)

# combine all messages  into a single string
text = ' '.join(df['messages'].dropna().astype(str).str.lower())

# define stopwords
stopwords = set(STOPWORDS)
custom_stopwords = {'https', 'http', 'discordapp', 'cdn', 'gif', 'tenor', 'togif',
                    'bro', 'u', 'im', 'ye', 'yeah', 'got', 'ur', 'sone', 'team',
                    'will', 'm', 'j', 't', 'pl', 'well', 're', 's', 'one', 'd', 'hes', 
                    'run'}
stopwords.update(custom_stopwords)

# Create the word cloud
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    max_words=600,
    stopwords=stopwords
).generate(text)

# display the word cloud
plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud.to_file(output_csv)
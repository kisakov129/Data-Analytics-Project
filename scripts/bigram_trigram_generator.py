import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path

input_csv = Path(__file__).parent.parent / 'processed_csvs' / 'messages.csv'
bigram_csv = Path(__file__).parent.parent / 'word_clouds' / 'bigram_wordcloud.png'
trigram_csv = Path(__file__).parent.parent / 'word_clouds' / 'trigram_wordcloud.png'

df = pd.read_csv(input_csv)

# extract messages
messages = df['messages'].dropna().astype(str).str.lower()

# use regex to remove 10 or move consecutive digits
# (probably a channel mention or something alike)
messages = messages.str.replace(r'\b\d{10,}\b', '', regex=True)

stopwords = set(STOPWORDS)
custom_stopwords = {
    'https', 'http', 'discordapp', 'cdn', 'gif', 'tenor', 'togif',
    'bro', 'u', 'im', 'ye', 'yeah', 'got', 'ur', 'net', 'attachments',
    'media', 'net', 'deleted', 'medal', 'tv', 'channels'
    'derppled', 'jbl', 'job', 'blurys', 'floofyflame', 'blurys',
    'delanoxd','nugdub', 'redd2', 'fawnaardvark', 'suitsnap',
    'swampgort', 'streetsharks', 'guide', 'gothmoney', 'shower'
}
stopwords.update(custom_stopwords)

# CountVectorizer tokenizes the text differently. i.e. 'aren't' is 'aren'
additional_stopwords = {
    'aren', 'couldn', 'didn', 'doesn', 'don', 'hadn',
    'hasn', 'haven', 'isn', 'let', 'll', 'mustn',
    're', 'shan', 'shouldn', 've', 'wasn', 'weren',
    'won', 'wouldn'
}
stopwords.update(additional_stopwords)

# extract bigrams and trigrams

bigram_vectorizer = CountVectorizer(
    stop_words=list(stopwords),
    ngram_range=(2, 2)
)

trigram_vectorizer = CountVectorizer(
    stop_words=list(stopwords),
    ngram_range=(3, 3)
)

# fit and transform the text
# basically gets a count for all the bigrams and trigrams in the text
# x for bigrams and y for trigrams
X = bigram_vectorizer.fit_transform(messages)
Y = trigram_vectorizer.fit_transform(messages)

# sum up the counts of each bigram/trigram
# for the counts we did in the previous step, we get a matrix and so we flatten it to an array using .A1
x_counts = X.sum(axis=0).A1
y_counts = Y.sum(axis=0).A1

# we got the counts from the previous step, so now we get the names
x_phrases = bigram_vectorizer.get_feature_names_out()
y_phrases = trigram_vectorizer.get_feature_names_out()

# create dictionary of {phrase: count}
x_phrase_freq = dict(zip(x_phrases, x_counts))
y_phrase_freq = dict(zip(y_phrases, y_counts))

wordcloud_x = WordCloud(
    width=1600,
    height=800,
    background_color='white'
).generate_from_frequencies(x_phrase_freq)

wordcloud_y = WordCloud(
    width=1600,
    height=800,
    background_color='white'
).generate_from_frequencies(y_phrase_freq)

plt.figure(figsize=(20, 10))
plt.imshow(wordcloud_x, interpolation='bilinear')
plt.axis('off')
plt.show()

plt.figure(figsize=(20, 10))
plt.imshow(wordcloud_y, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud_x.to_file(bigram_csv)
wordcloud_y.to_file(trigram_csv)

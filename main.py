# run from the project root with: 
# python main.py

import scripts.consolidate_to_csv
print("Finished consolidating JSON files.")

# uncomment this line to create cumulative message data:
# import scripts.get_and_filter_date

import scripts.get_mentions
print("Finished extracting mentions.")
import scripts.get_messages
print("Finished extracting messages.")
import scripts.mentions_generator
print("Finished generating mentions word cloud.")
import scripts.message_generator
print("Finished generating messages word cloud.")
import scripts.bigram_trigram_generator
print("Finished generating bigram and trigram word clouds.")
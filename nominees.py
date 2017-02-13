import numpy
from nltk.tag import pos_tag
tweets = numpy.load("tweetsarray.npy")

exclude_keys = [
'@GoldenGlobes',
'-',
'#GoldenGlobes',
'This',
'Picture',
'Picture,',
'An',
'RT',
'And',
'We',
'Motion',
'Television',
'Actor',
'Actress',
'Golden',
'Congrats',
'So,',
'Comedy',
'Performance'
]
award_titles = [
'Best Motion Picture Drama',
'Best Motion Picture Musical or Comedy',
'Best Director',
'Best Actor Motion Picture Drama',
'Best Actor Motion Picture Musical or Comedy',
'Best Actress Motion Picture Drama',
'Best Actress Motion Picture Musical or Comedy',
'Best Supporting Actor Motion Picture',
'Best Supporting Actress Motion Picture',
'Best Screenplay',
'Best Original Score',
'Best Original Song',
'Best Foreign Language Film',
'Best Animated Feature Film (since 2006)',
'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures',
'Best Drama Series',
'Best Comedy Series',
'Best Actor in a Television Drama Series',
'Best Actor in a Television Comedy Series',
'Best Actress in a Television Drama Series',
'Best Actress in a Television Comedy Series',
'Best Limited Series or Motion Picture made for Television',
'Best Actor in a Limited Series or Motion Picture made for Television',
'Best Actress in a Limited Series or Motion Picture made for Television',
'Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television',
'Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television',
]
# award_titles = [
# 'Drama',
# 'Musical or Comedy',
# 'Director',
# 'Actor Drama',
# 'Actor Musical or Comedy',
# 'Actress Motion Picture Drama',
# 'Actress Motion Picture Musical or Comedy',
# 'Supporting Actor',
# 'Supporting Actress',
# 'Screenplay',
# 'Original Score',
# 'Original Song',
# 'Foreign Language Film',
# 'Animated Feature Film',
# 'Cecil B. DeMille',
# 'Drama Series',
# 'Comedy Series',
# 'Television Drama Series',
# 'Television Comedy Series',
# 'Television Drama Series',
# 'Television Comedy Series',
# 'Limited Series or Motion Picture made for Television',
# 'Actor in a Limited Series or Motion Picture made for Television',
# 'Actress in a Limited Series or Motion Picture made for Television',
# 'Supporting Actor in a Series, Limited Series or Motion Picture made for Television',
# 'Supporting Actress in a Series, Limited Series or Motion Picture made for Television'
# ]


## filter_tweets
# Array of Str, Array of Dicts -> Array of Dicts
#
# Returns an array of tweet objects (dicts) whose text component contains at least one of the key words.
def filter_tweets(key_words, tweets):
  relevant_tweets = []
  for tweet in tweets:
    count = 0
    for key_word in key_words:

      # If the key word is in the text of the tweet, add it to the dict and break
      if ((key_word in tweet['tweet_text'])):
        count+=1
      else:
        break
      if (count == len(key_words)):
        relevant_tweets.append(tweet)
  return relevant_tweets

## filter_tweets
# Array of Str, Array of Dicts -> Array of Dicts
#
# Returns an array of tweet objects (dicts) whose text component contains at least one of the key words.
# def filter_tweets(key_words, tweets):
#   relevant_tweets = []
#   for tweet in tweets:
#     for key_word in key_words:
#       # If the key word is in the text of the tweet, add it to the dict and break
#       if ((key_word in tweet['tweet_text'])):
#         relevant_tweets.append(tweet)
#         break
#   return relevant_tweets

## determine_host
# Array of Str, Array of Dicts -> Str
#
# Returns the name most frequent bigram from the tweets filtered by key words.
def determine_nominees(key_words, tweets):
  relevant_tweets = filter_tweets(key_words, tweets)
  unigram_count = {}

  for tweet in relevant_tweets:
    unigrams = tweet['tweet_text'].split()
    tagged_sent = pos_tag(unigrams)
    # print tagged_sent
    propernouns = [word for word, pos in tagged_sent if pos == 'NNP']
    # print(propernouns)
    for unigram in unigrams:
      if ((unigram[0] == '@') or (unigram[0]) == '#' or (unigram in propernouns) and not (unigram in exclude_keys)):
        if unigram_count.has_key(unigram):
          unigram_count[unigram] += 1
        else:
          unigram_count[unigram] = 1
  return max_count_unigram(unigram_count)

## max_count
# Dict -> Str
#
# Returns the key with the largest associated value pair
def max_count(bigrams_count):
  max_count = 0
  host = ''
  if (not bigrams_count):
    return 'Could Not Determine Nominee'
  for bigram in bigrams_count.keys():
    if bigrams_count[bigram] > max_count:
      max_count = bigrams_count[bigram]
      host = bigram
  return (host[0] + ' ' + host[1])

def max_count_unigram(unigram_count):
  max_count = 0
  nominees = []
  if (not unigram_count):
    return 'Could Not Determine Nominees'
  for unigram in unigram_count.keys():
    # if unigram_count[unigram] > max_count:
    #   max_count = unigram_count[unigram]
    nominees.append(unigram)
    # else:
    #   continue

  return nominees

for award in award_titles:
  award_array = award.split()
  award_array.append('nominated')
  print(award + ' Nominees: ' + str(determine_nominees(award_array, tweets)))


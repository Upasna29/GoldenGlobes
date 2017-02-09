import numpy
tweets = numpy.load("tweetsarray.npy")

## filter_tweets
# Array of Str, Array of Dicts -> Array of Dicts
#
# Returns an array of tweet objects (dicts) whose text component contains at least one of the key words.
def filter_tweets(key_words, tweets):
  relevant_tweets = []

  for tweet in tweets:
    for key_word in key_words:
      # If the key word is in the text of the tweet, add it to the dict and break
      if ((key_word in tweet['tweet_text'])):
        relevant_tweets.append(tweet)
        break
  return relevant_tweets


## determine_host
# Array of Str, Array of Dicts -> Str
#
# Returns the name most frequent bigram from the tweets filtered by key words.
def determine_host(key_words, tweets):
  relevant_tweets = filter_tweets(key_words, tweets)
  bigrams_count = {}

  for tweet in relevant_tweets:
    # Make each tweet into bigram
    bigrams = zip(tweet['tweet_text'].split(), tweet['tweet_text'].split()[1:])

    for bigram in bigrams:
        # Only count the bigram if both words contain capitol letters
        if (not (bigram[0].isupper() or 
                 bigram[0].islower() or
                 bigram[1].isupper() or 
                 bigram[1].islower())):
          if bigrams_count.has_key(bigram):
            bigrams_count[bigram]+=1

          else:
            bigrams_count[bigram]=1
  return max_count(bigrams_count)

## max_count
# Dict -> Str
#
# Returns the key with the largest associated value pair
def max_count(bigrams_count):
  max_count = 0
  host = ''

  for bigram in bigrams_count.keys():
    if bigrams_count[bigram] > max_count:
      max_count = bigrams_count[bigram]
      host = bigram

  return (host[0] + ' ' + host[1])
    
##
# Future iterations of this project could train on tweets from other award ceremonies to 
# learn keywords associated with hosts
##
host = determine_host(['host'], tweets)

print('The host of this award ceremony was: ' + host)

print(determine_nominee(['Best'], tweets))
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

def determine_host(key_words, tweets):
  relevant_tweets = filter_tweets(key_words, tweets)
  twitter_handles = {}

  for tweet in relevant_tweets:
    for word in tweet['tweet_text'].split():
      if word.startswith('@'):
        if twitter_handles.has_key(word):
          twitter_handles[word] += 1
        else:
          twitter_handles[word] = 0
  return max_count(twitter_handles)


def max_count(twitter_handles):
  max_count = 0
  host_handle = ''

  for twitter_handle in twitter_handles.keys():
    if twitter_handles[twitter_handle] > max_count:
      max_count = twitter_handles[twitter_handle]
      host_handle = twitter_handle

  return host_handle
    

host = determine_host(['cold', 'open', 'host'], tweets)

print(host)

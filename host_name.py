f = open('globestweets.txt','r')
f = list(f)
usernames = list()

## filter_tweets
# Array of Str, Array of Dicts -> Array of Dicts
#
# Returns an array of tweet objects (dicts) whose text component contains at least one of the key words.
def filter_tweets(key_words, tweets):
  relevant_tweets = {}

  for tweet in tweets:
    for key_word in key_words:
      # If the key word is in the text of the tweet, add it to the dict and break
      if ((key_word in tweet['tweet_text'])):
        relevant_tweets[tweet['tweet_ID']] = tweet
        break
  return relevant_tweets

def host_name()

host_name(['cold', 'open', 'host'], 'Hi MY name is')
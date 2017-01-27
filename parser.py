import numpy
# RT @LaLaLand: Heres to the ones who dream. Congratulations to #LALALANDs Emma Stone for her #GoldenGlobes Best Actress win!  https://t.c	aRthur	505372294	818608286198992896	2017-01-09 23:59:59
# RT @VoteTrumpPics: Sylvester Stallone to @realDonaldTrump"To President Trump, A Real Champ! Greatest Knockout in History!" - @TheSlyStall	Kamehamedoukenn	2982913541	818608285712519168	2017-01-09 23:59:58
# RT @MyDaughtersArmy: Meryl Streep beautifully calls outs Donald Trump for mocking disabled reporter during her speech at #GoldenGlobeshttp	TC Ronaldinho	938301480	818608283376304128	2017-01-09 23:59:58

tweets_file = open("goldenglobes.tab", 'r');

# Structure of dictionary: {tweet_text: "", tweet_ID: ""}
tweets_array = []
prev_line = ""
for line in tweets_file:
    line = prev_line + line
    tokens = line.split('\t')
    if len(tokens) != 5:
        prev_line = line
    else:
        prev_line = ""
        tweet = {"tweet_text": tokens[0], "tweet_ID": tokens[3]}
        tweets_array.append(tweet)

numpy.savetxt("tweetsarray.txt", tweets_array, fmt = '%s')
numpy.save("tweetsarray.npy", tweets_array)
# result_array = numpy.load("tweetsarray.npy")

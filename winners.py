import numpy
import string
tweets = numpy.load("tweetsarray.npy")
count = 0

w_winners = list()
w_awards = list()


for each in tweets:
    index = list()
    if "18667907" in each["user_ID"] and "Congratulations to" in each["tweet_text"]:
        temp = each["tweet_text"].split(' ')
        for i, word in enumerate(temp):
            if word in ["-"]:
                index.append(i)
        if len(index) > 2:
            w_winners.append(temp[2:index[0]])
            w_awards.append(temp[index[0]+1:index[1]])

for i,each in enumerate(w_winners):
    for j,word in enumerate(each):
        if any(x in string.punctuation for x in word):
            del w_winners[i][j]
    if each == []:
        del w_winners[i]
        del w_awards[i]

w_spaces = list()



for each in w_winners:
    temp = ""
    for word in each:
        temp = temp+" "+word
    w_spaces.append(temp[1:])
w_winners = w_spaces
w_spaces = list()

for i,each in enumerate(w_awards):

    if each[0] == "":
        del w_awards[i][0]

    temp = ""
    for word in each:

        temp = temp+" "+word
    w_spaces.append(temp)
w_awards = w_spaces



for i, each in enumerate(w_winners):
    print w_awards[i] + " " +each

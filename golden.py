from collections import Counter,defaultdict
import numpy
import string
import nltk
import re
from difflib import SequenceMatcher

#adjust this number to improve accuracy
constant = 0.042#0.03409090909


tweets = numpy.load("tweetsarray.npy")


def similarRatio(a, b):
    """return percent simlarity between two strings
    Input: string, string
    Output: double"""
    return SequenceMatcher(None, a, b).ratio()

def checkSimilarOverList(s,l):
    """checks similarity of strings over list
    Input: string, list
    Output: bool"""
    for each in l:
        if similarRatio(s, each) > 0.80:
            return False
    return True

def getHandle(s):
    """Gets all twitter handles from a tweet
    Input: string
    Output: list of strings"""
    usernames = list()
    index = -1
    check = False
    for i,letter in enumerate(s):
        if check:
            if not(letter.isdigit() or letter.isalpha()):
                usernames.append(s[index:i])
                index = -1
                check = False
        else:
            if letter == '@':
                index = i
                check = True
    return usernames

def getCategory(s):
       """Gets category and returns as array if category is found in tweet
       Input: string
       Output: list of tuples of strings"""
       categories = list()
       index = -1
       check = False
       tweet = s.split(' ')
       for i, word in enumerate(tweet):
           if check:
               if word in ['at', 'for', 'win'] :
                   categories.append(tuple(tweet[index:i]))
                   index = -1
                   check = False
           else:
               if (len(tweet) >= i+2) and len(tweet[i+1])>0:
                   if word == 'Best' and tweet[i+1][0].isupper():
                       index = i
                       check = True
       if(len(categories)>0):
            return categories[0]

def categoryCount(c):
    """Counts categories and returns sorted list with frequency
    Input: list of tuples
    Output: list of tuples"""
    counts = Counter(c)
    categories = set(c)
    categories = list(categories)
    catecount = list()

    for each in categories:
        catecount.append((counts[each],each))

    catecount.sort(reverse = True)
    return catecount

def checkUppers(s):
    """Checks if a string has atleast two uppercase letters
    Input: string
    Ouput: bool"""
    count = 0
    for i, letter in enumerate(s):
        if letter.isupper():
            count = count +1
    return count > 1


def checkNameSize(s):
    """Checks the length of each name deciding if there should be spaces
    Input: string
    Output: bool"""
    index = -1
    smallest = 0
    for i, letter in enumerate(s):
        if letter.isupper() and index == -1:
            index = i
        elif letter.isupper():
            if smallest > i-index:
                smallest = i-index
    return smallest < 2

result = list()
catdict = {}
final = list()


for each in tweets:
    handles = list()
    category = getCategory(each['tweet_text'])
    if(category is not None):
        temp = ''
        result.append(category)
        for i in category:
            if(len(temp) == 0):
                temp = i
            else:
                temp = temp + ' ' + i
        if temp not in catdict.keys():
            catdict[temp] = {}

        handles = getHandle(each['tweet_text'])
        if len(handles) > 0:
            for handle in handles:
                catdict[temp][handle] = catdict[temp].get(handle, 0) + 1

        else:
            catdict.pop(temp, None)

        if 'goes to' in temp:
            final.append(temp)

freqCount = categoryCount(result)

awards = list()
names = list()
finaldict = {}
for i,each in enumerate(final):
    final[i].replace('/',' or ')
    index = final[i].find('goes to')
    final[i] = each[:index]+each[index+7:]
    names.append(each[index+7:])
    awards.append(each[:index])
    final[i] = final[i].translate(None, string.punctuation)
    tempname = each[index+7:]
    tempname = tempname.translate(None, string.punctuation)
    tempname = "".join(tempname.split())
    if checkUppers(tempname):
            tempname = re.sub(r"(\w)([A-Z])", r"\1 \2", tempname)
            if tempname not in finaldict.keys():
                finaldict[tempname] = {}
                finaldict[tempname][each[:index]] = finaldict[tempname].get(each[:index], 0) + 1


cate = list()
for each in final:
    cate.append(tuple(each.split(' ')))

for i,name in enumerate(names):
    names[i] = names[i].translate(None, string.punctuation)
    names[i] = "".join(names[i].split())


namesSet = set(names)
namesSet = list(names)
namesFreq = list()
for each in names:
    namesFreq.append(tuple(each.split(" ")))
namesFreq = categoryCount(namesFreq)

winners = list()

for each in namesFreq:
    if checkUppers(each[1][0]):
        if float(each[0]) > constant*float(len(namesFreq)):
            if checkSimilarOverList(each[1][0],winners):
                winners.append(re.sub(r"(\w)([A-Z])", r"\1 \2", each[1][0]))




for each in winners:
    print finaldict[each].keys()[0] +each

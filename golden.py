from collections import Counter,defaultdict
import numpy
import string
import nltk
import re
from difflib import SequenceMatcher

#adjust this number to improve accuracy
constant = 0.042#0.03409090909


tweets = numpy.load("tweetsarray.npy")
award_account_ID = '18667907'

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

def find_name(tweet_text):
    names = []
    bigrams = zip(tweet_text.split(" ")[:-1], tweet_text.split(" ")[1:])
    for bigram in bigrams:
        if len(bigram[0])>1 and len(bigram[1])>1:

            if bigram[0][0].isupper() and bigram[1][0].isupper():
                name = bigram[0] + ' ' + bigram[1]
                names.append(name)

    return names

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
    w_spaces.append(temp[1:])
w_awards = w_spaces

for i, each in enumerate(w_winners):
    if each not in finaldict.keys():
        print w_awards[i] + " " +each

print ""
print "Nominees"

nominees = """
Hacksaw Ridge
Hell or High Water
Lion
Manchester by the Sea
Moonlight
20th Century Women
Deadpool
La La Land
Florence Foster Jenkins
Sing Street
Casey Affleck
Joel Edgerton
Andrew Garfield
Viggo Mortensen   Captain Fantastic
Denzel Washington  Fences
Amy Adams  Arrival
Jessica Chastain  Miss Sloane
Isabelle Huppert  Elle
Ruth Negga  Loving
Natalie Portman  Jackie
Colin Farrell  The Lobster
Ryan Gosling  La La Land
Hugh Grant  Florence Foster Jenkins
Jonah Hill  War Dogs
Ryan Reynolds  Deadpool
Annette Bening  20th Century Women
Lily Collins  Rules Don't Apply
Hailee Steinfeld  The Edge of Seventeen
Emma Stone  La La Land
Meryl Streep  Florence Foster Jenkins
Mahershala Ali  Moonlight
Jeff Bridges  Hell or High Water
Simon Helberg  Florence Foster Jenkins
Dev Patel  Lion
Aaron Taylor-Johnson  Nocturnal Animals
Viola Davis  Fences
Naomie Harris  Moonlight
Nicole Kidman  Lion
Octavia Spencer  Hidden Figures
Michelle Williams  Manchester by the Sea
Damien Chazelle  La La Land
Tom Ford  Nocturnal Animals
Mel Gibson  Hacksaw Ridge
Barry Jenkins  Moonlight
Kenneth Lonergan  Manchester by the Sea
La La Land
Nocturnal Animals
Moonlight
Manchester by the Sea
Hell or High Water
Divines  France
Elle  France
Neruda  Chile
The Salesman  Iran/France
Toni Erdmann  Germany
Kubo and the Two Strings
Moana
My Life as a Zucchini
Sing
Zootopia
Can't Stop the Feeling  Trolls
City of Stars  La La Land
Faith  Sing
Gold  Gold
How Far I'll Go  Moana
Justin Hurwitz  La La Land
Johann Johannsson  Arrival
Dustin O'Halloran, Hauschka  Lion
Hans Zimmer, Pharrell Williams, Benjamin Wallfisch  Hidden Figures
The Crown
Game of Thrones
Stranger Things
This Is Us
Westworld
Atlanta
Black-ish
Mozart in the Jungle
Transparent
Veep
Rami Malek  Mr. Robot
Bob Odenkirk  Better Call Saul
Matthew Rhys  The Americans
Liev Schreiber  Ray Donovan
Billy Bob Thornton  Goliath
Caitriona Balfe  Outlander
Claire Foy  The Crown
Keri Russell  The Americans
Winona Ryder  Stranger Things
Evan Rachel Wood  Westworld
Anthony Anderson  Black-ish
Gael Garcia Bernal  Mozart in the Jungle
Donald Glover  Atlanta
Nick Nolte  Graves
Jeffrey Tambor  Transparent
Rachel Bloom  Crazy Ex-Girlfriend
Julia Louis-Dreyfus  Veep
Sarah Jessica Parker  Divorce
Issa Rae  Insecure
Gina Rodriguez  Jane the Virgin
Tracee Ellis Ross  Black-ish
American Crime
The Dresser
The Night Manager
The Night Of
The People v. O.J. Simpson: American Crime Story
Riz Ahmed  The Night Of
Bryan Cranston  All The Way
Tom Hiddleston  The Night Manager
John Turturro  The Night Of
Courtney B. Vance  The People v. O.J. Simpson: American Crime Story
Felicity Huffman  American Crime
Riley Keough  The Girlfriend Experience
Sarah Paulson  The People v. O.J. Simpson: American Crime Story
Charlotte Rampling  London Spy
Thandie Newton  Westworld
Olivia Colman  The Night Manager
Lena Headey  Game Of Thrones
Chrissy Metz  This Is Us
Mandy Moore  This Is Us
Kerry Washington  Confirmation
Sterling K. Brown  The People v. O.J. Simpson: American Crime Story
Hugh Laurie  The Night Manager
John Lithgow  The Crown
Christian Slater  Mr. Robot
John Travolta  The People v. O.J. Simpson: American Crime Story"""

noms = list()
for each in nominees.split("\n"):
    index = len(each)
    if each.find("  ") != -1:
        index = each.find("  ")
    noms.append(each[:index])

count = 0
n = 0
finalnoms = list()
actualnoms = list()
for each in tweets:
    for i,word in enumerate(each["tweet_text"].split(" ")):
        if word == "Nominee:":
            #print each["tweet_text"].split(" ")[i+1]
            efj = 0


    for nom in noms:
        if "nom" in each["tweet_text"] and "Best" not in each["tweet_text"] and "dress" not in each["tweet_text"]:
            temp = getHandle(each["tweet_text"])
            temp2 = find_name(each["tweet_text"])
            for i in temp2:
                finalnoms.append(i)
            for indv in temp:
                finalnoms.append(indv)
            count = count + 1
            break

counter = Counter(finalnoms)
for each in counter.keys():
    if counter[each] > 2:
        #print each
        n = n+ 1

for each in counter.most_common(126):
    print each[0]


print ""
print "Presenters"




gg_tweets = [t for t in tweets if t["user_ID"] == award_account_ID]
to_find = re.compile('https://|\!|\.|at|is ')


for t in gg_tweets:
    text = t["tweet_text"]
    names = []
    if (('present' or 'presents') in text) and ('Best' in text):

        name_start = text.find('Best ')
        match_obj = to_find.search(text, name_start)
        name_end = match_obj.start()
        cat_substr = text[name_start:name_end]
        if name_end != name_start:
            text = text[:name_start] + text[name_end:]
        else:
            text = text[:name_start]
        names = find_name(text)
        names.extend(getHandle(text))

        specifier = ''
        if 'nomin' in text:
            specifier = 'nomination to '
        if len(names)!=0:
            print 'Presenter(s) for ' + specifier + cat_substr + ': ' + ' '.join(names)

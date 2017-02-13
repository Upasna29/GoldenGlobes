import numpy
from collections import Counter

import string

def nameCounter(c):
    """Counts categories and returns sorted list with frequency
    Input: list of tuples
    Output: list of tuples"""
    counts = Counter(c)
    categories = set(c)
    categories = list(categories)
    namecount = list()

    for each in categories:
        namecount.append((counts[each],each))

    namecount.sort(reverse = True)
    return namecount


tweets = numpy.load("tweetsarray.npy")
"""
names = list()
for each in tweets:
    temp = each["tweet_text"].split(" ")
    for i, word in enumerate(temp):
        if word in ["presents"]:
            name = temp[i-2]+" "+temp[i-1]
            if len(temp[i-2])>0 and len(temp[i-1])>0:
                if temp[i-2][0].isupper() and temp[i-1][0].isupper():
                    if not(any(char in string.punctuation for char in name)):
                        names.append(tuple(name.split(" ")))

names = nameCounter(names)
namesfinal = list()
for each in names:
    namesfinal.append(""+each[1][0]+" "+each[1][1])
for each in namesfinal:
    print each


presenters = ["Kristen Wiig",
"Leonardo DiCaprio",
"Drew Barrymore,"
"Ben Affleck",
"Pierce Brosnan",
"Anna Kendrick",
"Naomi Campbell",
"Jessica Chastain",
"Steve Carell",
"Matt Damon",
"Reese Witherspoon",
"Zoe Saldana",
"Eddie Redmayne",
"Hugh Grant",
"Jon Hamm",
"Felicity Jones",
"Chris Hemsworth",
"John Legend",
"Ryan Reynolds",
"Sting",
"Emma Stone",
"Carrie Underwood",
"Vince Vaughn",
"Nicole Kidman",
"Carl Weathers",
"Amy Schumer",
"Brie Larson",
"Annette Benning",
"Viola Davis",
"Goldie Hawn",
"Sienna Miller",
"Diego Luna",
"Mandy Moore",
"Jeffrey Dean Morgan",
"Timothy Olyphant",
"Sofia Vergara",
"Chris Pine",
"Sylvester Stallone",
"Justin Theroux",
"Milo Ventimiglia"]
count = 0
for each in tweets:
    for presenter in presenters:
        if presenter in each["tweet_text"] and "dress" not in each["tweet_text"]:
            count = count + 1
            print each["tweet_text"]
            break

print count
"""

for each in tweets:
    if "What will you be eating while watching the #GoldenGlobes Red Carpet?" in each["tweet_text"] and "@goldenglobes" not in each["tweet_text"]:
        print each

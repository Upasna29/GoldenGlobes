import numpy
from collections import Counter
tweets = numpy.load("tweetsarray.npy")

nameOfEvent = "Golden Globes"

def find_name(tweet_text):
    names = list()
    bigrams = zip(tweet_text.split(" ")[:-1], tweet_text.split(" ")[1:])
    for bigram in bigrams:
        if len(bigram[0])>1 and len(bigram[1])>1:
            if bigram[0][0].isupper() and bigram[1][0].isupper():
                name = bigram[0] + ' ' + bigram[1]
                names.append(name)

    return names

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

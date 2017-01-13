f = open('globestweets.txt','r')
f = list(f)
usernames = list()

for each in  f:
    index = -1
    check = False
    for i,letter in enumerate(each):
        if check:
            if not(letter.isdigit() or letter.isalpha()):
                usernames.append(each[index:i])
                index = -1
                check = False
        else:
            if letter == '@':
                index = i
                check = True




usernames=set(usernames)
usernames = list(usernames)
usernames.sort()
print usernames

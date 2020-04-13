import smtplib, ssl, getpass
from random import randint

class Player:
    def __init__(self, email, name, code):
        self.email = email
        self.name = name
        self.code = code

    def printInfo(self):
        print(self.name + ": " + self.code)
    
    def getInfo(self):
        return str(self.name + ": " + self.code)

# get all emails from file
players = []
f = open('emails.txt', 'r')
lines = f.readlines()
for line in lines:
    info = line.split(' ')
    name = ''.join(info[0:len(info) - 1])
    email = info[-1][:-1]
    player = Player(email, name, "")
    players.append(player)

# get codes
codes = []
f = open('codes.txt', 'r')
lines = f.readlines()
for line in lines:
    codes.append(line)

# assign code to each player
codeSet = set()
for player in players:
    value = randint(0, len(codes)-1)
    while value in codeSet:
        value = randint(0, len(codes)-1)
    codeSet.add(value)
    word = codes[value]
    player.code = word

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
email = input("Please type your gmail username and press enter:")

sender_email = email + "@gmail.com"
receiver_email = "hbulmer@gmail.com"
password = getpass.getpass(prompt="Type your password and press enter: ")

print("Sending from " + sender_email)

def sendEmail(receiver, message):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

for i in range(len(players)):
    newPlayers = players.copy()
    player = newPlayers.pop(i)
    msg = """\
Subject: Headbandz

Dear """ + player.name + """,

Here is the Headbandz list for your game!

"""
    for p in newPlayers:
        msg += p.getInfo()
    
    sendEmail(player.email, msg)
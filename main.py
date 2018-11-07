# The only import you need!
import socket
import time
import random

# Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667  # port
# Options (Edit this)
# bot password can be found on https://twitchapps.com/tmi/
PASS = "oauth:2q1zxgr692whj2r6zgk01g8lzqo5nn"
BOT = "ssslon_bot"  # Bot's name [NO CAPITALS]
CHANNEL = "ssslon_"  # Channal name [NO CAPITALS]
OWNER = "zabroshenka"  # Owner's name [NO CAPITALS]

# Functions


def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())
    print("message sended")
    time.sleep(1.5)


def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def getMessage(line):
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message


def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
    sendMessage(s, "Chat room joined!")
    print("Bot has joined " + CHANNEL + " Channel!")


def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True
# Code runs


s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())
s = s_prep
joinchat()
readbuffer = ""


def Console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True


while True:
    try:
        readbuffer = s.recv(1024)
        readbuffer = readbuffer.decode()
        temp = readbuffer.split("\n")
        readbuffer = readbuffer.encode()
        readbuffer = temp.pop()
    except:
        temp = ""
    for line in temp:
        if line == "":
            break
        # So twitch doesn't timeout the bot.
        if "PING" in line and Console(line):
            msgg = "PONG tmi.twitch.tv\r\n".encode()
            s.send(msgg)
            print(msgg)
            break
        # get user
        user = getUser(line)
        # get message send by user
        message = getMessage(line)
        # for you to see the chat from CMD
        print(user + " > " + message)
        # sends private msg to the user (start line)
        PMSG = "/w " + user + " "

# for making commands

        randomn = random.randint(0, 10000)
        if user == OWNER and "!command" in message:
            mes = "im the best %d " % randomn
            sendMessage(s, mes)
            break
        elif "!private" in message.lower():
            mes = "private message %d " % randomn
            sendMessage(s, PMSG + mes)
            break
        elif "!ты" in message.lower():
            mes = "ti p1d0r @%s %d" % (user, randomn)
            print(mes)
            print(type(mes))
            sendMessage(s, mes)
            break
        elif "!global" in message.lower():
            mes = "global %d" % randomn
            sendMessage(s, mes)
            break
        else:
            mes = "wtf %d" % randomn
            sendMessage(s, mes)
            break
############################################################################

import socket
import time
# from new import Bot

class Run():
    def __init__(self, password, bot, channel, owner):
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667  # port
        self.PASS = password
        self.BOT = bot
        self.CHANNEL = channel
        self.OWNER = owner


    def getMessage(self, line):
        try:
            self.message = (line.split(":", 2))[2]
        except:
            self.message = ""
        return self.message

    def Console(self, line):
        # gets if it is a user or twitch server
        if "PRIVMSG" in line:
            return False
        else:
            return True


    def getUser(self, line):
        separate = line.split(":", 2)
        self.user = separate[1].split("!", 1)[0]
        return self.user

    def loadingCompleted(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

    def joinchat(self):
        readbuffer_join = "".encode()
        Loading = True
        while Loading:
            readbuffer_join = self.s.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            self.temp = readbuffer_join.split("\n")
            readbuffer_join = readbuffer_join.encode()
            readbuffer_join = self.temp.pop()
            for line in self.temp:
                Loading = self.loadingCompleted(line)
        print("Bot has joined " + self.CHANNEL + " Channel!")

    def connect(self):
        s_prep = socket.socket()
        s_prep.connect((self.SERVER, self.PORT))
        s_prep.send(("PASS " + self.PASS + "\r\n").encode())
        s_prep.send(("NICK " + self.BOT + "\r\n").encode())
        s_prep.send(("JOIN #" + self.CHANNEL + "\r\n").encode())
        self.s = s_prep
        self.joinchat()
        readbuffer = ""
        return self.s


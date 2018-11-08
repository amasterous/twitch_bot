from initbot import Run
import time
from settings import PASS, BOT, CHANNEL, OWNER
from db import DB


class Bot(Run):
    # def __init(self):
    #     super(Bot, self).__init__()
    #     self.db = DB('twitch.db')
    #     self.commands = self.db.get_commands()

    def start(self):
        self.connect()
        self.db = DB('twitch.db')
        self.commands = self.db.get_commands()
        # self.sendMessage(self.s, ("Connected to %s " % self.CHANNEL))
        self.messageHandler()

    def parse_help(self, commands):
        print(self.commands())

    def messageController(self, message):
        print(message)
        for command in self.commands:
            if "!help" in message:
                mes = "Команды для чата: "
                for com in self.commands:
                    description = self.db.get_description(com)
                    mes += "%s - % s :: " % (com, description)
                self.sendMessage(mes)
                break
            if command in message:
                print("message = command")
                self.sendMessage(self.db.get_action(command))
                break


    def messageHandler(self):
        while True:
            try:
                readbuffer = self.s.recv(1024)
                readbuffer = readbuffer.decode()
                self.temp = readbuffer.split("\n")
                readbuffer = readbuffer.encode()
                readbuffer = self.temp.pop()
            except:
                self.temp = ""
            for line in self.temp:
                if line == "":
                    break
                # So twitch doesn't timeout the bot.
                if "PING" in line and self.Console(line):
                    msgg = "PONG tmi.twitch.tv\r\n".encode()
                    self.s.send(msgg)
                    print(msgg)
                    break
                # get user
                self.user = self.getUser(line)
                # get message send by user
                message = self.getMessage(line)
                # for you to see the chat from CMD
                print(self.user + " > " + message)
                # sends private msg to the user (start line)
                self.messageController(message)
                # if "!stop" in message:
                #     exit()
                #     # TODO1 читать .todo
                # else:
                #     print("not exit")

    def sendMessage(self, message):
        messageTemp = "PRIVMSG #" + self.CHANNEL + " :" + message
        self.s.send((messageTemp + "\r\n").encode())
        print("message \"%s\" sended" % message)
        time.sleep(1.5)

    def sendPrivateMessage(self, s, message):
        self.PMSG = "/w " + self.user + " "
        messageTemp = "PRIVMSG #" + self.CHANNEL + " :" + self.PMSG + message
        s.send((messageTemp + "\r\n").encode())
        print("message \"%s\" sended" % message)
        # time.sleep(1.5)


bot = Bot(PASS, BOT, CHANNEL, OWNER)


bot.start()

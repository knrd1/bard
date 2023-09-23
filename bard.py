from bardapi import Bard
from bardapi import BardCookies
import socket
import ssl
import time
import configparser
from typing import Union, Tuple

# Read configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up Google cookies

cookie_dict = {
    "__Secure-1PSID": config['cookies']['__Secure-1PSID'],
    "__Secure-1PSIDTS": config['cookies']['__Secure-1PSIDTS'],
}

bard = BardCookies(cookie_dict=cookie_dict)

# Set up IRC connection settings
server = config.get('irc', 'server')
port = config.getint('irc', 'port')
usessl = config.getboolean('irc', 'ssl')
channels = config.get('irc', 'channels').split(',')
nickname = config.get('irc', 'nickname')
ident = config.get('irc', 'ident')
realname = config.get('irc', 'realname')
password = config.get('irc', 'password')

# Connect to IRC server
def connect(server, port, usessl, password, ident, realname, nickname, channels):
    while True:
        try:
            print("Connecting to: " + server)
            irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            irc.connect((server, port))
            if usessl:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                irc = context.wrap_socket(irc, server_hostname=server)
            if password:
                irc.send(bytes("PASS " + password + "\n", "UTF-8"))
            irc.send(bytes("USER " + ident + " 0 * :" + realname + "\n", "UTF-8"))
            irc.send(bytes("NICK " + nickname + "\n", "UTF-8"))
            print("Connected to: " + server)
            return irc
        except:
            print("Connection failed. Retrying in 5 seconds...")
            time.sleep(5)

irc = connect(server, port, usessl, password, ident, realname, nickname, channels)

# Listen for messages from users and answer questions
while True:
    try:
        data = irc.recv(4096).decode("UTF-8")
        if data:
            print(data)
    except UnicodeDecodeError:
        continue
    except:
        print("Connection lost. Reconnecting...")
        time.sleep(5)
        irc = connect(server, port, usessl, password, ident, realname, nickname, channels)
    irc.send(bytes("JOIN " + ",".join(channels) + "\n", "UTF-8"))
    chunk = data.split()
    if len(chunk) > 0:
        if data.startswith(":"):
            command = chunk[1]
        else:
            command = chunk[0]
        if command == "PING":
            irc.send(bytes("PONG " + chunk[1] + "\n", "UTF-8"))
        elif command == "ERROR":
            print("Received ERROR from server. Reconnecting...")
            time.sleep(5)
            irc = connect(server, port, usessl, password, ident, realname, nickname, channels)
        elif command == "471" or command == "473" or command == "474" or command == "475":
            print("Unable to join " + chunk[3] + ": Channel can be full, invite only, bot is banned or needs a key.")
        elif command == "KICK" and chunk[3] == nickname:
            irc.send(bytes("JOIN " + chunk[2] + "\n", "UTF-8"))
            print("Kicked from channel " + chunk[2] + ". Rejoining...")
        elif command == "INVITE":
            if data.split(" :")[1].strip() in channels:
                irc.send(bytes("JOIN " + data.split(" :")[1].strip() + "\n", "UTF-8"))
                print("Invited into channel " + data.split(" :")[1].strip() + ". Joining...")
        elif command == "PRIVMSG" and chunk[2].startswith("#") and chunk[3] == ":" + nickname + ":":
            channel = chunk[2].strip()
            question = data.split(nickname + ":")[1].strip()
            try:
                response = bard.get_answer(question)['content']
                answers = [x.strip() for x in response.strip().split('\n')]
                for answer in answers:
                    while len(answer) > 0:
                        if len(answer) <= 392:
                            irc.send(bytes("PRIVMSG " + channel + " :" + answer + "\n", "UTF-8"))
                            answer = ""
                        else:
                            last_space_index = answer[:392].rfind(" ")
                            if last_space_index == -1:
                                last_space_index = 392
                            irc.send(bytes("PRIVMSG " + channel + " :" + answer[:last_space_index] + "\n", "UTF-8"))
                            answer = answer[last_space_index:].lstrip()
            except Exception as e:
                print("Error: " + str(e))
                irc.send(bytes("PRIVMSG " + channel + " :BARD PANIC! Check console for error message.\n", "UTF-8"))
    else:
        continue
    time.sleep(1)

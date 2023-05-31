import json
import string
import random
import requests
from .message import Listen


def username_gen(length=24, chars= string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))  


def password_gen(length=8, chars= string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(length))  


class Email(Listen):
    token = ""
    domain = ""
    address = ""
    session = requests.Session()
    def __init__(self, proxypath):
        if proxypath:
            with open(proxypath, 'r') as file:
                proxies_list = file.read().splitlines()
            proxy = random.choice(proxies_list).split(':')
            proxies = {
                'http': f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
                'https': f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
            }
            self.proxies = proxies
        else:
            pass

    def register(self, username=None, password=None, token=False):
        self.domain = 'internetkeno.com'
        username = username if username else username_gen()
        self.password = password if password else password_gen()

        url = "https://api.mail.tm/accounts"
        payload = {
            "address": f"{username}@{self.domain}",
            "password": self.password
        }
        headers = { 'Content-Type': 'application/json' }
        response = self.session.post(url, headers=headers, json=payload, proxies=self.proxies)
        response.raise_for_status()

        data = response.json()
        try:
            self.address = data['address']
        except:
            self.address = f"{username}@{self.domain}"
        if token:
            self.get_token(self.password)

        if not self.address:
            raise Exception("Failed to make an address")

    def get_token(self, password):
        url = "https://api.mail.tm/token"
        payload = {
            "address": self.address,
            "password": password
        }
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        try:
            self.token = response.json()['token']
        except:
            raise Exception("Failed to get token")
        

if __name__ == "__main__":
    def listener(message):
        print("\nSubject: " + message['subject'])
        print("Content: " + message['text'] if message['text'] else message['html'])

    # Get Domains
    test = Email()
    print("\nDomain: " + test.domain)

    # Make new email address
    test.register()
    print("\nEmail Adress: " + str(test.address))

    # Start listening
    test.start(listener)
    print("\nWaiting for new emails...")

    # Stop listening
    # test.stop()

import requests
import re
import urllib.request
import socket
from pprint import pprint
import configparser
import twitter


def check_url(url, timeout=5 ):
    try:
        return urllib.request.urlopen(url,timeout=timeout).getcode() == 200
    except urllib.request.URLError as e:
        return False
    except socket.timeout as e:
        return False


def get_scihub_mirrors_up():
    mirrorsUp = []
    wiki_url = "https://en.wikipedia.org/wiki/Sci-Hub"
    res = requests.get(wiki_url)
    hrefs = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', res.text)
    links = []
    for href in hrefs:
        if 'sci-hub' in href:
            links.append(href)
    for url in links:
        if check_url(url):
            mirrorsUp.append(url)
    return mirrorsUp


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    consumer_key = config['twitter_connect']['consumer_key']
    consumer_secret = config['twitter_connect']['consumer_secret']
    access_token = config['twitter_connect']['access_token']
    access_token_secret = config['twitter_connect']['access_token_secret']

    print(consumer_key)
    print(consumer_secret)
    print(access_token)
    print(access_token_secret)

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

    urls = get_scihub_mirrors_up()
    pprint(urls)

    message = '🚀 Sci-hub mirrors available today:'
    for url in urls:
        message = message+"\n- {}".format(url)

    print(message)
    try:
        status = api.PostUpdate(message)
    except UnicodeDecodeError:
        print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
        print("Try explicitly specifying the encoding with the --encoding flag")

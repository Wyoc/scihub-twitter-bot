import requests
import re
import urllib.request
import socket
from pprint import pprint


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

    urls = get_scihub_mirrors_up()
    pprint(urls)
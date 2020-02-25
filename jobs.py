import time
import re
import requests
import os
import base64
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def url_to_page_name(url):
    parsed = urlparse(str(url))
    return parsed.netloc


def get_text_job(page_url):
    """
        Request given page and extract text
    """
    directory_name = url_to_page_name(page_url)

    response = requests.get(page_url).text
    # create a new bs4 object from the html data loaded
    soup = BeautifulSoup(response, 'html.parser')

    # remove all javascript and stylesheet code
    for script in soup(["script", "style"]):
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    save_path = os.path.join(f'{directory_name}/' + "text.txt")
    with open(save_path, 'w', encoding="utf-8") as f:
        f.write(text)


def get_images_job(page_url):
    """
        Request given page and extract images
    """
    time.sleep(10)
    print(page_url)


def long_job(duration):
    time.sleep(duration)
    return {'job': True}


if __name__ == "__main__":
    # testing
    get_text_job("https://www.google.com/")

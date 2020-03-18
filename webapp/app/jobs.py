import time
import re
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mimetypes
from selenium import webdriver
import uuid

CHROME_DRIVER_PATH = '../../chromedriver_win32/chromedriver.exe'


def fix_bad_file_name(file_name):
    """
        Replace corrupted file name with a generated id
    """
    file_name_extension = re.search(r"(\..*)$", file_name).group(1)
    file_name = str(uuid.uuid1().int)
    return "unknown_name_" + file_name + file_name_extension


def url_to_page_name(url):
    parsed = urlparse(str(url))
    return parsed.netloc


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_image_name_from_url(url):
    a = urlparse(url)
    return os.path.basename(a.path)


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
    directory_name = url_to_page_name(page_url)
    browser = webdriver.Chrome(CHROME_DRIVER_PATH)

    browser.get(page_url)
    data = BeautifulSoup(browser.page_source, 'html.parser')

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # All the Src
    for src in data.find_all('img'):
        url = src['src']

        file_name = get_image_name_from_url(url)

        # Sometimes an image source can be relative if it is provide the base url which also happens to be the site variable atm.
        if 'http' not in url:
            url = '{}{}'.format(page_url, url)

        response = requests.get(url)

        if bool(re.search(r"(\..*)$", file_name)) is False:
            # The type is in the content-type header. For mapping this to a file extension use mimetypes
            type = response.headers['Content-Type']
            type = mimetypes.guess_extension(type, strict=True)

            try:
                file_name = file_name + type
            except TypeError:
                # Unknown type (type=None)
                pass

        try:
            with open(os.path.join(f'{directory_name}/' + file_name), 'wb') as f:
                f.write(response.content)
        except OSError:
            # Invalid name
            file_name = fix_bad_file_name(file_name)
            with open(os.path.join(f'{directory_name}/' + file_name), 'wb') as f:
                f.write(response.content)
        except Exception:
            pass

    # That's all folks
    browser.quit()


def long_job(duration):
    time.sleep(duration)
    return {'job': True}


if __name__ == "__main__":
    pass
    # testing
    get_images_job("https://www.google.pl")

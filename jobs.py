import time
import re
import requests
import os
import base64
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import imghdr


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
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    soup = BeautifulSoup(requests.get(page_url).content, "html.parser")

    urls = []
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        img_url = urljoin(page_url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

            # finally, if the url is valid
        if is_valid(img_url):
                urls.append(img_url)

    print(urls)
    for url in urls:
        #file_name = re.search(r'/([\w_-]+[.](jpg|gif|png|jpeg|webp))$', url)

        file_name = get_image_name_from_url(url)

        with open(os.path.join(f'{directory_name}/' + file_name), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(page_url, url)
            response = requests.get(url)
            f.write(response.content)


def get_images_with_src(page_url):
    """Request given page and extract images"""

    directory_name = url_to_page_name(page_url)

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for url in urls:
        file_name = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)

        if file_name:
            file_name = file_name.group(1)

            with open(os.path.join(f'{directory_name}/' + file_name), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative
                    # if it is provide the base url which also happens
                    # to be the site variable atm.
                    url = '{}{}'.format(page_url, url)
                response = requests.get(url)
                f.write(response.content)


def long_job(duration):
    time.sleep(duration)
    return {'job': True}


if __name__ == "__main__":
    # testing
    #get_text_job("https://www.google.com/")

    get_images_job("https://www.wp.pl/")
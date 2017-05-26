import urllib.request, urllib.error
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from re import search

domain_regex_front = '^https://exponea.com'
base_url = 'https://exponea.com'
urls = [base_url]
checked_urls = []
images = []

valid = URLValidator()


def process_url(url: str, validator: URLValidator, domain_regex: str) -> []:

    print('Processing url: %s' % url)

    # invalid URL format
    try:
        validator(url)
    except ValidationError:
        print('Incorrect URL')
        return [], []

    # not our domain
    if not bool(search(domain_regex, url)):
        print('URL does not respond to domain specified')
        return [], []

    # HTTP request denied
    try:
        with urllib.request.urlopen(url) as response:

            # check for html content
            content_type = response.getheader('Content-Type')
            if not bool(search('.*html.*', content_type)):
                print('Non-html content')
                return [], []

            html = response.read()

    except urllib.error.HTTPError:
        print('HTTP request denied')
        return [], []

    soup = BeautifulSoup(html, 'html.parser')

    fetched_urls = [link['href'] for link in soup.find_all('a', href=True)]
    fetched_images = [link['src'] for link in soup.find_all('img', src=True)]

    return fetched_urls, fetched_images


while len(urls) > 0:

    print('Queue size: %d' % len(urls))
    print('Checked urls: %d' % len(checked_urls))

    actual_url = urls[0]
    checked_urls.append(urls.pop(0))
    print('Added ')

    new_urls, new_images = process_url(actual_url, valid, domain_regex_front)

    # we need to check both queue and old urls
    urls += [url for url in new_urls if
             (url not in checked_urls) and
             (url not in urls)]
    images += [image for image in new_images if image not in images]

print('Amount of images found: %d' % len(images))






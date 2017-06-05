import urllib
import logging
from re import search
from urllib import request, error

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from image_crawler.download_handle import DownloadHandle


class ImageCrawler(object):
    """
    Crawls images from given url
    Stays within specified domains
    Images are saved into working directory, under subfolder specified in property file
    """

    def crawl_images(self, start_url, permitted_domains, dir_save):
        url_crawler = self.UrlCrawler(permitted_domains)

        urls = {start_url}
        checked_urls = set()
        images = set()
        dl_handle = DownloadHandle()

        while urls:

            next_url = urls.pop()
            new_urls, new_images = url_crawler.crawl_url(next_url)
            checked_urls.add(next_url)

            urls.update(new_urls - checked_urls)
            images.update(new_images)

        for url in images:
            dl_handle.download_image(url, dir_save)

        logging.info('Crawling images finished')

    class UrlCrawler(object):

        def __init__(self, permitted_domains):
            self.permitted_domains = permitted_domains
            self.url_validator = URLValidator()

        def crawl_url(self, url: str):

            html_content = self._get_content(url)

            if not html_content:
                return set(), set()

            soup = BeautifulSoup(html_content, 'html.parser')

            fetched_urls = {link['href'] for link in soup.find_all('a', href=True)}
            fetched_images = {link['src'] for link in soup.find_all('img', src=True)}

            return fetched_urls, fetched_images

        def _url_verify(self, url):

            try:
                self.url_validator(url)
            except ValidationError:
                logging.error('Incorrect format of URL: {:40}'.format(url))
                return False

            return self._target_domain_verify(url)

        def _get_content(self, url):

            if not self._url_verify(url):
                return None

            try:
                with urllib.request.urlopen(url) as response:
                    if bool(search('.*html.*', response.getheader('Content-Type'))):
                        return response.read()

            except urllib.error.HTTPError:
                logging.error('HTTP request denied at URL: {:40}'.format(url))
                return None

            except urllib.error.URLError:
                logging.error('HTTP request failed at URL: {:40}'.format(url))
                logging.info('Check Internet connection or proxy settings')
                return None

            return None

        def _target_domain_verify(self, url):

            if any([url.startswith(domain) for domain in self.permitted_domains]):
                return True
            else:
                logging.info('No match for permitted domains at URL: {:40}'.format(url))
                return False

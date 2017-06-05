import urllib
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

    def __init__(self):
        self.url_validator = URLValidator()

    def crawl_images(self, start_url, permitted_domains, dir_save, log):

        urls = {start_url}
        checked_urls = set()
        images = set()
        dl_handle = DownloadHandle()

        while urls:

            next_url = urls.pop()
            new_urls, new_images = self._crawl_url(next_url, permitted_domains, log)
            checked_urls.add(next_url)

            urls = urls.union(new_urls - checked_urls)
            images = images.union(new_images)

        for url in images:
            dl_handle.download_image(url, dir_save, log)

        log.info('Crawling images finished')

    def _crawl_url(self, url: str, permitted_domains: [], log):

        html_content = self._get_content(url, permitted_domains, log)

        if not html_content:
            return set(), set()

        soup = BeautifulSoup(html_content, 'html.parser')

        fetched_urls = {link['href'] for link in soup.find_all('a', href=True)}
        fetched_images = {link['src'] for link in soup.find_all('img', src=True)}

        return fetched_urls, fetched_images

    def _url_verify(self, url, permitted_domains, log):

        try:
            self.url_validator(url)
        except ValidationError:
            log.error('Incorrect format of URL: {:40}'.format(url))
            return False

        return self._target_domain_verify(url, permitted_domains, log)

    def _get_content(self, url, permitted_domains, log):

        if not self._url_verify(url, permitted_domains, log):
            return None

        try:
            with urllib.request.urlopen(url) as response:
                if bool(search('.*html.*', response.getheader('Content-Type'))):
                    return response.read()

        except urllib.error.HTTPError:
            log.error('HTTP request denied at URL: {:40}'.format(url))
            return None

        except urllib.error.URLError:
            log.error('HTTP request failed at URL: {:40}'.format(url))
            log.info('Check Internet connection or proxy settings')
            return None

        return None

    @staticmethod
    def _target_domain_verify(url, permitted_domains, log):

        if any([bool(search('^'+domain, url)) for domain in permitted_domains]):
            return True
        else:
            log.info('No match for permitted domains at URL: {:40}'.format(url))
            return False

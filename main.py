import config
from image_crawler.image_crawler import ImageCrawler

crawler = ImageCrawler()
config.log_init()

crawler.crawl_images(config.start_url, config.domain_permissions, config.dir_target)

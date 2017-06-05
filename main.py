from image_crawler.logging_handle import LoggingHandle
import config
from image_crawler.image_crawler import ImageCrawler

crawler = ImageCrawler()
log = LoggingHandle(config.dir_logging)

crawler.crawl_images(config.start_url, config.domain_permissions, config.dir_target, log)

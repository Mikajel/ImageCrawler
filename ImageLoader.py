import Properties as Prop
from ExpoCrawler import ImageCrawler
from FileHandler import LoggingHandle

crawler = ImageCrawler()
log = LoggingHandle(Prop.dir_logging)

crawler.crawl_images(Prop.start_url, Prop.domain_permissions, Prop.dir_target, log)











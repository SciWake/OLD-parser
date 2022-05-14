from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from review import settings
from review.spiders.otzovik import OtzovikSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(OtzovikSpider)
    crawler_process.start()

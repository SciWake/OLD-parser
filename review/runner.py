from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from review import settings
from review.spiders.irecommend import IrecommendSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(IrecommendSpider)
    crawler_process.start()

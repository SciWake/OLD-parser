import scrapy


# from ghost import Ghost

class IrecommendSpider(scrapy.Spider):
    name = 'irecommend'
    allowed_domains = ['irecommend.ru']
    start_urls = ['https://irecommend.ru/catalog/list/31']

    def start_requests(self):
        # Cookie - это строка cookie, полученная после входа в систему.
        cookies = 'ab_var=9; _ym_uid=1642182277111621385; _ym_d=1650790107; ss_uid=16507901074258828; _ga=GA1.1.471788507.1650790107; v=fc; stats_s_a=nQLabnyAzHUjvFrVin%2FNY4zvpxU6yP1mLGyFId0iwBgJ7II%2FUeQYY9SHWOET6VilqH8crf7q0R5ssxRt3HrkbOFG4q4DQ%2B%2BHtugaODIrgZyEhRfyjV3H9ZvGG9zUU4Rktezif5iyia5kSPVx%2FVlLbmPUPxM053Fc0%2FjRVyv2aedbw%2FUsLXr361IbEGfz7sDHwVCxgJFD4UucOHu8oVym4XamyvrrUAknyqTg9yuLe9a4vQwYZjOqxtwLq9VauVuZtgiS2wmmkYo%3D; stats_u_a=TvoYVZvdZYFvh9%2BZitqd66F9dmiG362BqgPxo7ucGUAxKe0in2M4AK%2FM%2BYDBwq6Y7U%2BAWnV0A37Kwgb2om2ft6IkD%2BydlnC%2F%2BaJfXsuns20%3D; _ym_isad=1; _gid=GA1.1.1414163064.1652375890; _ym_visorc=b'
        # Преобразовать в словарь
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        # headers = {"Cookie":cookies}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies  # переносить cookies для запроса
            # headers = headers
        )

    def parse(self, response):
        # Getting base pagination links
        for page_url in response.css('div.item-list ul.pager li.pager-item a::attr("href")'):
            yield response.follow(page_url, callback=self.parse)

        # Getting links to product
        for product_url in response.css('div.view-content div.ProductTizer a.reviewsLink::attr("href")'):
            yield response.follow(product_url, callback=self.parse_review)
        print(1)

    # def parse_product(self, response):
    #     # Getting product pagination links
    #     for prod_page_url in response.css('div.item-list ul.pager li a::attr("href")'):
    #         yield response.follow(prod_page_url, callback=self.parse_product)
    #
    #     # Getting links to review
    #     for review_url in response.css('div.item-list ul.list-comments li.item div.reviewTitle a::attr("href")'):
    #         yield response.follow(review_url, callback=self.parse_review)

    def parse_review(self, response):
        print(1)

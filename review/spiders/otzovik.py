import scrapy


class OtzovikSpider(scrapy.Spider):
    name = 'otzovik'
    allowed_domains = ['otzovik.com']
    start_urls = ['https://otzovik.com/health/fragrance']
    cookies = [{'domain': '.otzovik.com', 'expiry': 1652418908, 'httpOnly': False, 'name': 'csid', 'path': '/',
                'secure': False, 'value': '3594085729'},
               {'domain': '.otzovik.com', 'expiry': 1683954901, 'httpOnly': False, 'name': '_ym_uid', 'path': '/',
                'secure': False, 'value': '1652418902444858460'},
               {'domain': '.otzovik.com', 'expiry': 1683954901, 'httpOnly': False, 'name': '_ym_d', 'path': '/',
                'secure': False, 'value': '1652418902'},
               {'domain': '.otzovik.com', 'expiry': 1715577301, 'httpOnly': True, 'name': 'ssid', 'path': '/',
                'secure': False, 'value': '3594085729'},
               {'domain': '.otzovik.com', 'expiry': 1683954901, 'httpOnly': False, 'name': 'refreg', 'path': '/',
                'secure': False,
                'value': '1652418901~https%3A%2F%2Fotzovik.com%2Fhealth%2Ffragrance%2F%3F%26capt4a%3D1831652418894304'},
               {'domain': '.otzovik.com', 'expiry': 1652490901, 'httpOnly': False, 'name': '_ym_isad', 'path': '/',
                'secure': False, 'value': '2'},
               {'domain': '.otzovik.com', 'httpOnly': True, 'name': 'ROBINBOBIN', 'path': '/', 'secure': False,
                'value': 'a0a27080ee9d68f02132dfc36d'}]

    def start_requests(self):
        # Cookie - это строка cookie, полученная после входа в систему.
        cookiesa = 'ab_var=9; _ym_uid=1642182277111621385; _ym_d=1650790107; ss_uid=16507901074258828; _ga=GA1.1.471788507.1650790107; v=fc; stats_s_a=nQLabnyAzHUjvFrVin%2FNY4zvpxU6yP1mLGyFId0iwBgJ7II%2FUeQYY9SHWOET6VilqH8crf7q0R5ssxRt3HrkbOFG4q4DQ%2B%2BHtugaODIrgZyEhRfyjV3H9ZvGG9zUU4Rktezif5iyia5kSPVx%2FVlLbmPUPxM053Fc0%2FjRVyv2aedbw%2FUsLXr361IbEGfz7sDHwVCxgJFD4UucOHu8oVym4XamyvrrUAknyqTg9yuLe9a4vQwYZjOqxtwLq9VauVuZtgiS2wmmkYo%3D; stats_u_a=TvoYVZvdZYFvh9%2BZitqd66F9dmiG362BqgPxo7ucGUAxKe0in2M4AK%2FM%2BYDBwq6Y7U%2BAWnV0A37Kwgb2om2ft6IkD%2BydlnC%2F%2BaJfXsuns20%3D; _ym_isad=1; _gid=GA1.1.1414163064.1652375890; _ym_visorc=b'
        # Преобразовать в словарь
        cookiesa = {i.split("=")[0]: i.split("=")[1] for i in cookiesa.split("; ")}
        # headers = {"Cookie":cookies}
        print(1)
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=self.cookies  # переносить cookies для запроса
            # headers = headers
        )

    def parse(self, response):
        # Getting base pagination links
        for page_url in response.css('div.pager a.nth::attr("href")'):
            yield response.follow(page_url, callback=self.parse)

        # Getting links to product
        for product_url in response.css('div.product-list tr a.product-name::attr("href")'):
            yield response.follow(product_url, callback=self.parse_product)

    def parse_product(self, response):
        # Getting product pagination links
        for prod_page_url in response.css('div.pager a.nth::attr("href")'):
            yield response.follow(prod_page_url, callback=self.parse_product)

        # Getting links to review
        for review_url in response.css('div.review-list-chunk div.mshow0 a.review-read-link::attr("href")'):
            yield response.follow(review_url, callback=self.parse_review)

    def parse_review(self, response):
        data = {
            'title': response.css('div.product-header a.product-name span::text')[0].extract(),

        }
        yield data

import requests
import bs4
from time import sleep

BASE_URL = 'https://irecommend.ru'
url = 'https://irecommend.ru/catalog/list/31'

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}

cookies = 'ab_var=9; _ym_uid=1642182277111621385; _ym_d=1650790107; ss_uid=16507901074258828; _ga=GA1.1.471788507.1650790107; v=fc; stats_s_a=nQLabnyAzHUjvFrVin%2FNY4zvpxU6yP1mLGyFId0iwBgJ7II%2FUeQYY9SHWOET6VilqH8crf7q0R5ssxRt3HrkbOFG4q4DQ%2B%2BHtugaODIrgZyEhRfyjV3H9ZvGG9zUU4Rktezif5iyia5kSPVx%2FVlLbmPUPxM053Fc0%2FjRVyv2aedbw%2FUsLXr361IbEGfz7sDHwVCxgJFD4UucOHu8oVym4XamyvrrUAknyqTg9yuLe9a4vQwYZjOqxtwLq9VauVuZtgiS2wmmkYo%3D; stats_u_a=TvoYVZvdZYFvh9%2BZitqd66F9dmiG362BqgPxo7ucGUAxKe0in2M4AK%2FM%2BYDBwq6Y7U%2BAWnV0A37Kwgb2om2ft6IkD%2BydlnC%2F%2BaJfXsuns20%3D; _ym_isad=1; _gid=GA1.1.1414163064.1652375890; _ym_visorc=b'
cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}


def get_page(url):
    while url:
        print(url)
        response = requests.get(url, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        yield soup
        url = get_next_page(soup)


def get_next_page(soup: bs4.BeautifulSoup) -> str:
    a = soup.select_one('div.bloko-gap a.HH-Pager-Controls-Next')
    return f'{BASE_URL}{a["href"]}' if a else None


if __name__ == '__main__':
    for soup in get_page(url):
        print(1)

import csv
import os
import random
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumChrome:
    def __init__(self):
        self.browser = self.settings_browser()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def settings_browser(self) -> webdriver.Chrome:
        """Возвращает конфигурированный драйвер."""
        return webdriver.Chrome(options=self.get_selenium_options(), executable_path=self.get_path_webdriver())

    def get_selenium_options(self) -> Options:
        """
        Установка основных настроек chrome driver.
        :return: Настройки барузера
        """
        # УДАЛИТЬ ВЫВОД В ФИНАЛЬНОЙ РЕАЛИЗАЦИИ
        user_agent = self.get_user_agent()
        print(user_agent)

        options = Options()
        # Selenium settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-urlfetcher-cert-requests')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument(f'user-agent=Mozilla Firefox 36 (Win 8.1 x64): Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0')

        # options.add_argument(f'--proxy-server=socks4://{self.proxy[0]}:{self.proxy[1]}')
        # options.add_argument('--headless')
        # options.add_argument('--window-size=1920,1080')
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        return options

    @staticmethod
    def get_path_webdriver() -> str:
        """
        Метод возвращет путь до webdriver в зависимости от операционной системы.
        :return: Путь до webdriver
        """
        if platform.system().lower() == "windows":
            return os.path.join(os.getcwd(), "selenium_chrome", "driver", "chromedriver_win.exe")
        elif platform.system().lower() == "linux":
            return os.path.join(os.getcwd(), "selenium_chrome", "driver", "chromedriver_linux")
        return os.path.join(os.getcwd(), "selenium_chrome", "driver", "chromedriver_macos")

    @staticmethod
    def get_user_agent() -> str:
        """Возвращает случайный user-agent для браузера."""
        with open(os.path.join(os.getcwd(), "selenium_chrome", "user_agents.csv")) as csv_file:
            return ''.join(random.choice(list(csv.reader(csv_file))))

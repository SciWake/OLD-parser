import os
import time
import pickle
from selenium_chrome import SeleniumChrome


class UpdateCookies(SeleniumChrome):

    def __init__(self, url):
        super().__init__()
        self.url = url

        with open(os.path.join(os.getcwd(), 'cookies.pickle'), 'rb') as f:
            self.cookies = pickle.load(f)

    def captcha_checking(self):
        time.sleep(2)
        # Checking for the presence of a captcha on the page
        while len(self.browser.find_elements_by_css_selector('tbody h1')):
            time.sleep(1)

    def load_page(self):
        self.browser.get(self.url)
        time.sleep(1)
        for cookie in self.cookies:
            self.browser.add_cookie(cookie)
        self.browser.get(self.url)
        self.captcha_checking()

    def update_cookies(self):
        pickle.dump(self.browser.get_cookies(), open(f"cookies.pickle", "wb"))  # update cookies
        self.browser.quit()

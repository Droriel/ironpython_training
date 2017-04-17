# -*- coding: utf-8 -*-
from selenium import webdriver
from fixture.session import SessionHelper


class Application:

    def __init__(self, browser, base_url):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'edge':
            self.wd = webdriver.Edge()
        else:
            raise ValueError('Unrecognized browser %s' % browser)
        # self.wd.implicitly_wait(5)
        # w tej aplikacji nie ma potrzeby - czeka zadaną ilość sekund na pojawienie się elementu
        self.session = SessionHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def change_field_value(self, field_name, text):
        if text is not None:
            self.wd.find_element_by_name(field_name).click()
            self.wd.find_element_by_name(field_name).clear()
            self.wd.find_element_by_name(field_name).send_keys(text)



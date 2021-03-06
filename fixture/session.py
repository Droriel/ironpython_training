# -*- coding: utf-8 -*-
from selenium.webdriver.support.wait import WebDriverWait


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        # Fill in username
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        # Fill in password
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_xpath("//input[@value='Login']").click()
        # waiting for the refresh of content
        wait = WebDriverWait(wd, 10)
        wait.until(lambda d: d.find_element_by_xpath("//td[@class='login-info-left']"))
        if not self.is_logged_in():
            raise ValueError()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href,'logout_page.php')]").click()

    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//td[@class='login-info-left']/span[1]").text

    def is_logged_in(self):
        wd = self.app.wd
        # return len(wd.find_elements_by_xpath("//td[@class='login-info-left']")) > 0
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)

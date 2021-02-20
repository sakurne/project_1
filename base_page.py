 
mport datetime
import os
from abc import abstractmethod, ABC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from locators import BaseLocators

from lib_patches.wait import WebDriverWait
import settings
import random


class BasePage(ABC):
    def __init__(self, app, open_page=True, full_url=True):
        self.app = app
        if open_page:
            if app.browser.current_url != self.base_url:
                self.app.open_page(self.base_url)
                if full_url:
                    self.wait_url()
                else:
                    self.url_contains(self.base_url)
        else:
            self.url_contains(self.base_url)
        self.skeleton_built()
        app.current_page = self

    @property
    @abstractmethod
    def base_url(self):
        pass

    def wait_url(self, url=None):
        if not url:
            url = self.base_url
        return WebDriverWait(
            self.app.browser,
            settings.DEFAULT_TIMEOUT
        ).until(lambda _: self.app.browser.current_url == url)

    def url_contains(self, url_part, timeout=settings.DEFAULT_TIMEOUT):
        browser = self.app.browser
        WebDriverWait(browser, timeout).until(EC.url_contains(url_part))

    def is_element_present(self, how, what):
        browser = self.app.browser
        browser.implicitly_wait(0)
        try:
            return len(browser.find_elements(how, what)) > 0
        finally:
            browser.implicitly_wait(settings.DEFAULT_IMPLICITLY_WAIT)

    def fill_input_field(self, how, what, content, clear=True):
        browser = self.app.browser
        field = browser.find_element(how, what)
        if clear:
            field.clear()
        text_len = len(self.get_attribute_from_element(how, what))
        if text_len:
            field.send_keys('\b' * text_len)
        field.send_keys(content)

    def clear_field(self, how, what):
        browser = self.app.browser
        field = browser.find_element(how, what)
        text_len = len(self.get_attribute_from_element(how, what))
        if text_len:
            field.send_keys('\b' * text_len)
            
        def find_when_appeared(self, how, what, timeout=settings.DEFAULT_TIMEOUT):
        browser = self.app.browser
        element = WebDriverWait(
            browser,
            timeout,
            settings.DEFAULT_POLL_FREQUENCY
        ).until(EC.presence_of_element_located((how, what)))
        return element

    def find_elements(self, how, what):
        return self.app.browser.find_elements(how, what)
    
        def find_elements_when_appeared(self, how, what, timeout=settings.DEFAULT_TIMEOUT):
        browser = self.app.browser
        WebDriverWait(browser, timeout).until(EC.presence_of_all_elements_located((how, what)))
        return self.app.browser.find_elements(how, what)

    def count_of_elements(self, how, what, error_message='', timeout=settings.DEFAULT_TIMEOUT):
        try:
            length = len(self.find_elements_when_appeared(how, what, timeout=timeout))
        except TimeoutException:
            raise AssertionError(error_message)
        return length
    
        def check_and_click(
            self,
            how, what,
            error_message="",
            by_cursor=False,
            timeout=settings.DEFAULT_TIMEOUT,
            scroll=False,
            check_clickability=False,
    ):
        try:
            self.find_when_appeared(how, what, timeout=timeout)
            self.click_element(how, what, by_cursor=by_cursor, scroll=scroll, check_clickability=check_clickability)
        except TimeoutException:
            raise AssertionError(error_message)

    def check_and_fill(self, how, what, keys, error_message=None, timeout=settings.DEFAULT_TIMEOUT, clear=True):
        try:
            self.find_when_appeared(how, what, timeout=timeout)
        except TimeoutException:
            raise AssertionError(error_message)
        self.fill_input_field(how, what, keys, clear=clear)

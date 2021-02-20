from pages.base_page import BasePage
from pages.clinic_page import ClinicPage
from locators import BaseLocators, ServicePricesLocators
from elements.base_elements import VDialog
from utils import price_format
import settings
import random


class ServicePricesPage(BasePage):
    base_url = settings.SERVICE_PRICES_URL

    def __init__(self, app):
        super(ServicePricesPage, self).__init__(app)
        self.keyboard_dialog = VDialog(self.app, BaseLocators.V_DIALOG_ACTIVE)

    def choose_section(self, text):
        self.check_and_click(*BaseLocators.DIV_CONTAINS_TEXT(text), 'section name is not right')
        self.skeleton_built()
        
    
    def click_buttons_services(self, element_name):
        if element_name == '+':
            self.check_and_click(*ServicePricesLocators.PLUS_ICON, 'plus icon is not found', check_clickability=True)
        elif (element_name in settings.SERVICES_NOT_AVAILABLE_FOR_BOOKING) or (
                element_name in ['Удалить оборудование', 'Хорошо', 'Подтвердить', 'Удалить услугу']
        ):
            self.check_and_click(*BaseLocators.SPAN_CONTAINS_TEXT(element_name), check_clickability=True)
        elif element_name == 'Удалить':
            self.check_and_click(*ServicePricesLocators.APPROVE_DELETE_SERVICE_BUTTON, check_clickability=True)
            self.skeleton_built()
            self.notify_disappeared()
            return
        else:
            self.check_and_click(
                *BaseLocators.DIV_CONTAINS_TEXT(element_name),
                '"{}" button is not found'.format(element_name),
                check_clickability=True
            )
        self.skeleton_built()
        
    def choose_any_service(self):
        listitems_len = self.count_of_elements(*BaseLocators.LISTITEM_XPATH)
        rand_index = random.randint(1, listitems_len - 1)
        self.app.created_service = self.check_and_get_attribute(
            *BaseLocators.LISTITEM_BY_INDEX(rand_index),
            'innerText'
        ).split('\n')[0]
        self.check_and_click(*BaseLocators.LISTITEM_BY_INDEX(rand_index))
        self.skeleton_built()
        
     def choose_existing_service(self):
        self.app.created_service = self.check_and_get_attribute(
            *BaseLocators.LISTITEM_BY_INDEX(1),
            'innerText'
        ).split('\n')[0]
        self.check_and_click(*BaseLocators.LISTITEM_BY_INDEX(1))

    def fill_price(self, price):
        self.keyboard_dialog.fill_price_by_keyboard(price)

    def success_msg_here(self):
        assert self.should_be_element(*BaseLocators.DIV_CONTAINS_TEXT('Услуга добавлена')), 'success message not found'
        assert self.should_be_element(*BaseLocators.DIV_CONTAINS_TEXT(
            '{} - {}'.format(self.app.created_service, self.app.created_service_price)
        )), 'success message is not right'

    def service_exists(self, name=None, price=None):
        if not name:
            name = self.app.created_service
        if not price:
            price = self.app.created_service_price
        assert self.should_be_element(
            *ServicePricesLocators.SERVICE_BY_NAME_PRICE(name, price.strip())
        ), 'service is not added'
        
    def service_not_exists(self, name=None):
        if not name:
            name = self.app.created_service
        assert self.should_not_be_element(
            *ServicePricesLocators.SERVICE_BY_NAME(name)
        ), 'service is still here'

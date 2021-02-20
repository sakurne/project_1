 from lib_patches.bdd_allure import when, then, scenarios, given
from pytest_bdd import parsers
from pages.service_prices_page import ServicePricesPage
from pages.clinic_page import ClinicPage


scenarios('../features/service_prices.feature')


@given(parsers.cfparse('Открыт раздел "Личный кабинет" - "Цены на услуги" - "{section_name}"'))
def opened_section(logged_in_app_clinics_for_prices, section_name):
    ServicePricesPage(logged_in_app_clinics_for_prices).choose_section(section_name)
    
@when(parsers.cfparse('Нажимаем "{element_name}"'))
def click_buttons_services(logged_in_app_clinics_for_prices, element_name):
    logged_in_app_clinics_for_prices.current_page.click_buttons_services(element_name)
    
@when(parsers.cfparse('Выбираем категорию "{category_name}"'))
def choose_section(logged_in_app_clinics_for_prices, category_name):
    logged_in_app_clinics_for_prices.current_page.choose_subsection(category_name)


@when(parsers.cfparse('Выбираем любую услугу'))
def choose_any_service(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.choose_any_service()
    
@when(parsers.cfparse('Вводим стоимость {price} рублей'))
@when(parsers.cfparse('Вводим стоимость {price} рубля'))
def fill_price(logged_in_app_clinics_for_prices, price):
    logged_in_app_clinics_for_prices.created_service_price = price
    logged_in_app_clinics_for_prices.current_page.fill_price(price)
    
@then('Появилось сообщение об успешно добавленной услуге')
def success_msg_here(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.success_msg_here()


@then(parsers.cfparse('Услуга отображается в разделе "Личный кабинет" - "Цены на услуги" - "{section_name}"'))
def service_presented(logged_in_app_clinics_for_prices, section_name):
    ServicePricesPage(logged_in_app_clinics_for_prices).choose_section(section_name)
    logged_in_app_clinics_for_prices.current_page.service_exists()
    
@then('Услуга больше недоступна при добавлении новой услуги')
def service_cant_be_added(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.service_cant_be_added()
    
@then(parsers.cfparse('Услуга отображается на странице клиники с правильной стоимостью'))
def service_presented_in_clinic(logged_in_app_clinics_for_prices):
    ClinicPage(logged_in_app_clinics_for_prices).check_price()
    
@when('Вводим стоимость, отличную от существующей')
def change_price(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.change_price()
    
@then('Цена услуги изменилась')
def price_changed(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.price_changed()
    
@then('Услуга больше не присутствует в списке')
def service_not_exists(logged_in_app_clinics_for_prices):
    logged_in_app_clinics_for_prices.current_page.service_not_exists()

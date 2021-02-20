 import pytest
from utils import login_prodoctorov
from pages.cabinet_page import CabinetPage
from data_base.db_adapter import DataBase
from data_base.db_objects.lpu import LPU
import random


@pytest.fixture
def app(selenium_, tmpdir):
    browser = Application(
        selenium=selenium_,
        tmp_dir=str(tmpdir)
    )
    yield browser
    return browser


@pytest.fixture
def mobile_app(app):
    assert MOBILE_FIXTURES_LIST, 'Список фикстуры для мобильной версии пуст!'
    return app

def login_fixture_common_step(mobile_app, login):
    login_pd(mobile_app, login=login)
    lpu_link = CabinetPage(mobile_app).get_clinic_url()
    print('Clinic page address: {}'.format(mobile_app.lpu.lpu_link))
 
 
@pytest.fixture
def logged_in_app_clinics_for_prices(mobile_app):
    login_fixture_common_step(mobile_app, login=random.choice(DataBase().get_clinics_for_prices()))
    yield mobile_app
    return mobile_app

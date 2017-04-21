# -*- coding: utf-8 -*-
import json
import os.path
import pytest
from fixture.application import Application
import importlib
import jsonpickle
from fixture.db import DbFixture
# from fixture.orm import ORMFixture
import ftputil

fixture = None
configuration = None


def load_config(file):
    global configuration
    if configuration is None:
        # __file__ wskazuje lokalizację bieżącego pliku, ale może być absolutna lub względna
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file)
        with open(config_file) as config:
            configuration = json.load(config)
    return configuration


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption('--configuration'))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    return fixture


@pytest.fixture(scope="session")
def db(request, config):
    db_config = config['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.backup"):
            remote.remove("config_inc.php.backup")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.backup")
        remote.upload(os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.backup"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.backup", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture



# @pytest.fixture(scope="session")
# def orm(request):
#     db_config = load_config(request.config.getoption('--configuration'))['db']
#     ormfixture = ORMFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])
#     # def fin():
#     #     ormfixture.destroy()
#     # request.addfinalizer(fin)
#     return ormfixture


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--configuration', action='store', default='configuration.json')
    parser.addoption('--check_ui', action='store_true')


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testData = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testData, ids=[str(x) for x in testData])
        elif fixture.startswith("json_"):
            testData = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testData, ids=[str(x) for x in testData])


def load_from_module(module):
    return importlib.import_module('data.%s' % module).testData


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/%s.json" %file)) as f:
        return jsonpickle.decode(f.read())




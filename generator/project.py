# -*- coding: utf-8 -*-
import random
import string
from model.project import Project
import jsonpickle
import os.path
import sys
import getopt

try:
    opts, args=getopt.getopt(sys.argv[1:], 'n:f:', ['number of projects', 'file'])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = 'data/projects.json'

for o, a in opts:
    if o == '-n':
        n = int(a)
    elif o == '-f':
        f = a
# opcje wpisujemy w opcje skryptu "-n 10 -f data/test,json"


def random_string(prefix, maxlen):
    # symbols = string.ascii_letters + string.digits + string.punctuation + ' '*10
    symbols = string.ascii_letters + string.digits + ' ' * 15 + '\n' * 5 + '-' * 3 + '_' * 3
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def random_string_without_breaklines(prefix, maxlen):
    # symbols = string.ascii_letters + string.digits + string.punctuation + ' '*10
    symbols = string.ascii_letters + string.digits + ' ' * 15 + '-' * 3 + '_' * 3
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testData = [Project(name=random_string_without_breaklines("Nazwa ", 10), status='', inherit_categories='', view_status='', description='')] + \
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=10, inherit_categories=0, view_status=10, description=random_string("Opis: ", 10))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=10, inherit_categories=1, view_status=50, description=random_string("Opis: ", 20))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=30, inherit_categories=0, view_status=10, description=random_string("Opis: ", 10))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=30, inherit_categories=1, view_status=50, description=random_string("Opis: ", 20))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=50, inherit_categories=0, view_status=10, description=random_string("Opis: ", 20))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=50, inherit_categories=1, view_status=50, description=random_string("Opis: ", 10))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=70, inherit_categories=0, view_status=10, description=random_string("Opis: ", 20))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=70, inherit_categories=1, view_status=50, description=random_string("Opis: ", 10))] +\
[Project(name=random_string_without_breaklines("Nazwa ", 10), status=70, inherit_categories=0, view_status=50, description='')]


file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..' , f)

with open(file, 'w', encoding='utf8') as out:
    jsonpickle.set_encoder_options('json', indent=2)
    out.write(jsonpickle.encode(testData))
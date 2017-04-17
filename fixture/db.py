# -*- coding: utf-8 -*-
import random
from re import sub

import pymysql.cursors
# import mysql.connector

from model.project import Project
# from model.contact import ContactAllData, ContactBaseData, PhoneNumbers

def delete_break_line(s):
    return sub("\n", ' ', s)

class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_project_list(self):
        list =[]
        cursor = self.connection.cursor()
        # sprawdzić czy można zamiast poniższego użyć kontrukcji with
        try:
            cursor.execute('select name, status, inherit_global, view_state, description from mantis_project_table')
            for row in cursor:
                (name, status, inherit_categories, view_status, description) = row
                list.append(Project(name=name, status=status, inherit_categories=inherit_categories, view_status=view_status, description=delete_break_line(description)))
        finally:
            cursor.close()
        return list

    # def get_one_project(self):
    #     list = []
    #     cursor = self.connection.cursor()
    #     # sprawdzić czy można zamiast poniższego użyć kontrukcji with
    #     try:
    #         cursor.execute('select name, status, inherit_global, view_state, description from mantis_project_table limit 1')
    #         for row in cursor:
    #             (name, status, inherit_categories, view_status, description) = row
    #             list.append(
    #                 Project(name=name, status=status, inherit_categories=inherit_categories, view_status=view_status,
    #                         description=description))
    #     finally:
    #         cursor.close()
    #     return list

    def get_one_project(self):
        list = []
        cursor = self.connection.cursor()
        # sprawdzić czy można zamiast poniższego użyć kontrukcji with
        try:
            cursor.execute('select name, status, inherit_global, view_state, description from mantis_project_table')
            for row in cursor:
                (name, status, inherit_categories, view_status, description) = row
                list.append(
                    Project(name=name, status=status, inherit_categories=inherit_categories, view_status=view_status,
                            description=description))
        finally:
            cursor.close()
        return random.choice(list)


    # def get_contact_list(self):
    #     list =[]
    #     cursor = self.connection.cursor()
    #     # sprawdzić czy można zamiast poniższego użyć kontrukcji with
    #     try:
    #         cursor.execute('select id, firstname, lastname, address, home, mobile, work, phone2, email, email2, email3 from addressbook where deprecated="0000-00-00 00:00:00"')
    #         for row in cursor:
    #             (id, firstname, lastname, address, homephone, mobilephone, workphone, additionalphone, email1, email2, email3) = row
    #             contactBaseData = ContactBaseData(id=str(id), firstname=firstname, lastname=lastname, address=address,
    #                                               homephone=homephone, mobilephone=mobilephone, workphone=workphone, additionalphone=additionalphone,
    #                                               email1=email1, email2=email2, email3=email3)
    #             list.append(ContactAllData(contactBaseData=contactBaseData, personalData='', phoneNumbers='',
    #                                        emails='',www='', additionalData='', notes='', birthDate='', anniversaryDate=''))
    #     finally:
    #         cursor.close()
    #     return list

    def destroy(self):
        self.connection.close()
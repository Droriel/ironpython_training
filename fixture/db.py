# -*- coding: utf-8 -*-
import random
from test_adds import adjustement

import pymysql.cursors
# import mysql.connector

from model.project import Project


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
                list.append(Project(name=name, status=status, inherit_categories=inherit_categories, view_status=view_status, description=adjustement.delete_break_line_DB(description)))
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

    def destroy(self):
        self.connection.close()
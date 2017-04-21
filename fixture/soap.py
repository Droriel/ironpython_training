from suds.client import Client
from suds import WebFault

from model.project import Project
from test_adds import adjustement


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client('http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        client = Client('http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl')
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            # print(projects)
            list=[]
            for project in projects:
                name = project['name']
                status = project['status']['id']
                # if project['inherit_global'] == True:
                #     inherit_categories = 1
                # elif project['inherit_global'] == False:
                #     inherit_categories = 0
                view_status = project['view_state']['id']
                if project['description'] == None:
                    description = ""
                else:
                    description = str(project['description'])
                # description = str(project['description'])
                list.append(Project(name=name, status=status, inherit_categories=1, view_status=view_status, description=adjustement.delete_break_line_soap(description)))
            return list
        except WebFault:
            return False
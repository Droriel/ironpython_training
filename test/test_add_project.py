from re import sub

from selenium.webdriver.support.wait import WebDriverWait
from model.project import Project

def delete_break_line(s):
    return sub("\n", ' ', s)

def test_add_project(app, db, json_projects):
    app.project.open_create_page()
    old_projects = db.get_project_list()
    project = json_projects
    app.project.fill_project_data(name=project.name, status=project.status, inherit_categories=project.inherit_categories, view_status=project.view_status,
                                  description=project.description)
    app.project.submit_project()
    wait = WebDriverWait(app.wd, 10)
    # wait.until(lambda d: d.find_element_by_xpath("//input[@value='Create New Project']"))
    wait.until(lambda d: d.find_element_by_link_text("Proceed"))
    app.wd.find_element_by_link_text("Proceed").click()
    wait.until(lambda d: d.find_element_by_xpath("//input[@value='Create New Project']"))
    assert app.wd.find_element_by_link_text("%s" % project.name)
    new_projects = db.get_project_list()
    assert len(old_projects) +1 == len(new_projects)
    project.description = delete_break_line(project.description)
    old_projects.append(project)
    # assert sorted(old_projects, key=Project.name) == sorted(new_projects, key=Project.name)
    # assert sorted(old_projects, key=Project.lower_name) == sorted(new_projects, key=Project.lower_name)
    print(old_projects)
    print(new_projects)
    assert sorted(old_projects, key=Project.get_name) == sorted(new_projects, key=Project.get_name)
    # assert old_projects == new_projects


def test_add_existing_project(app, db):
    app.project.open_create_page()
    old_projects = db.get_project_list()
    project = db.get_one_project()
    app.project.fill_project_data(name=project.name, status=50, inherit_categories=False, view_status=50,
                                  description='To jest opis 1')
    app.project.submit_project()
    wait = WebDriverWait(app.wd, 10)
    new_projects = db.get_project_list()
    assert len(old_projects) == len(new_projects)
    wait.until(lambda d: d.find_element_by_xpath("//td[contains(.,'APPLICATION ERROR #701')]"))
    assert app.wd.find_element_by_xpath("//p[contains(.,'A project with that name already exists. Please go back and enter a different name.')]")
    assert old_projects == new_projects


# def test_empty_project_name(app):
# def test_directly after login

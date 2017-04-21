import random
import string



def random_string_without_breaklines(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + ' ' * 15 + '-' * 3 + '_' * 3
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_delete_project(app, db):
    app.session.ensure_login("administrator", "root")
    if len(db.get_project_list())==0:
        app.project.open_create_page()
        app.project.fill_name(name=random_string_without_breaklines("Nazwa ", 10))
        app.project.submit_project()
    app.project.open_manage_projects_page()
    # old_projects = db.get_project_list()
    old_projects = app.soap.get_project_list("administrator", "root")
    project = db.get_one_project()
    app.project.delete_project(project.name)
    # new_projects = db.get_project_list()
    new_projects = app.soap.get_project_list("administrator", "root")
    assert len(old_projects) -1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects


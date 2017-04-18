from selenium.webdriver.support.wait import WebDriverWait


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('/manage_proj_page.php')
                and len(wd.find_elements_by_xpath("//input[@value='Create New Project']")) > 0
                ):
            wd.find_element_by_link_text('Manage').click()
            wait = WebDriverWait(wd, 10)
            wait.until(lambda d: d.find_element_by_xpath("//a[contains(.,'Manage Projects')]"))
            wd.find_element_by_link_text('Manage Projects').click()
            wait.until(lambda d: d.find_element_by_xpath("//input[@value='Create New Project']"))

    def open_create_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('/manage_proj_create_page.php')
                and len(wd.find_elements_by_xpath("//input[@value='Add Project']")) > 0
                ):
            wd.find_element_by_link_text('Manage').click()
            wait = WebDriverWait(wd, 10)
            wait.until(lambda d: d.find_element_by_xpath("//a[contains(.,'Manage Projects')]"))
            wd.find_element_by_link_text('Manage Projects').click()
            wait.until(lambda d: d.find_element_by_xpath("//input[@value='Create New Project']"))
            wd.find_element_by_xpath("//input[@value='Create New Project']").click()
            wait.until(lambda d: d.find_element_by_xpath("//input[@value='Add Project']"))

    def fill_project_data(self, name, status, inherit_categories, view_status, description):
        wd = self.app.wd
        self.fill_name(name=name)
        self.fill_status(status=status)
        self.fill_inherit_global_categories(inherit_categories=inherit_categories)
        self.fill_view_status(view_status=view_status)
        self.fill_description(description=description)

    def fill_name(self, name):
        wd = self.app.wd
        self.app.change_field_value(field_name='name', text=name)
        # wd.find_element_by_name('name').click()
        # wd.find_element_by_name('name').clear()
        # wd.find_element_by_name('name').send_keys(name)

    def fill_status(self, status):
        wd = self.app.wd
        wd.find_element_by_name('status').click()
        wait = WebDriverWait(wd, 10)
        wait.until(lambda d: d.find_element_by_xpath("//select[@name='status']/option[@value='10']"))
        # development
        if status == 10:
            wd.find_element_by_xpath("//select[@name='status']/option[@value='10']").click()
        # release
        elif status == 30:
            wd.find_element_by_xpath("//select[@name='status']/option[@value='30']").click()
        # stable
        elif status == 50:
            wd.find_element_by_xpath("//select[@name='status']/option[@value='50']").click()
        # obsolete
        elif status == 70:
            wd.find_element_by_xpath("//select[@name='status']/option[@value='70']").click()

    def fill_inherit_global_categories(self, inherit_categories=1):
        wd = self.app.wd
        if inherit_categories == 0:
            if wd.find_element_by_name('inherit_global').is_selected():
                wd.find_element_by_name('inherit_global').click()
        elif inherit_categories == 1 or inherit_categories is None:
            if not wd.find_element_by_name('inherit_global').is_selected():
                wd.find_element_by_name('inherit_global').click()

    def fill_view_status(self, view_status):
        wd = self.app.wd
        wd.find_element_by_name('view_state').click()
        # 'public'
        if view_status == 10:
            wd.find_element_by_xpath("//select[@name='view_state']/option[@value='10']").click()
        # 'private'
        elif view_status == 50:
            wd.find_element_by_xpath("//select[@name='view_state']/option[@value='50']").click()

    def fill_description(self, description):
        wd = self.app.wd
        # self.app.change_field_value(field_name='description', text=description)
        wd.find_element_by_name('description').click()
        wd.find_element_by_name('description').clear()
        wd.find_element_by_name('description').send_keys(description)

    def submit_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def open_project(self, name):
        wd = self.app.wd
        wd.find_element_by_link_text('%s' % name).click()
        wait = WebDriverWait(wd, 10)
        wait.until(lambda d: d.find_element_by_xpath("//input[@value='Delete Project']"))

    def delete_project(self, name):
        wd = self.app.wd
        self.open_project(name)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wait = WebDriverWait(wd, 10)
        wait.until(lambda d: d.find_element_by_xpath("//div[contains(.,'Are you sure you want to delete this project and all attached issue reports?Project Name: %s')]" %name))
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wait.until(lambda d: d.find_element_by_xpath("//input[@value='Create New Project']"))





import re



class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        self.app.change_field_value(field_name='username', text=username)
        self.app.change_field_value(field_name='email', text=email)
        # wd.find_element_by_xpath("//input[@value='Signup']").click()
        wd.find_element_by_xpath("//input[@type='submit']").click()

        #odebranie maila
        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        wd.get(url)
        self.app.change_field_value(field_name='password', text=password)
        self.app.change_field_value(field_name='password_confirm', text=password)
        wd.find_element_by_xpath("//input[@value='Update User']").click()

    def extract_confirmation_url(self, text):
        # return re.search(".*http:.*", text)
        # miltiline powoduje że jako text traktowana jest jego linia $ koniec linii nie całego stringa
        return re.search("http://.*$", text, re.MULTILINE).group(0)



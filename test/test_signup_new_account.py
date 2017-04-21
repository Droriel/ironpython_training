import random
import string


def random_string_simple(maxlen):
    symbols = string.ascii_letters + string.digits + ' '*13 + '-'*3 + '_'*3
    #                      + "'"*3
    return ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_username(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + '-'*3 + '_'*3 + "."*3
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_signup_new_account(app):
    username = random_username("user_", 10)
    password = "test"
    email=username + '@localhost'
    # nie robimy odrębnej fixtury dla serwera pocztowego tylko dodatkowy helper do fixtury application (tak samo jak przy session)
    app.james.ensure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    # sprawdzenie w aplikacji
    # app.session.login(username, password)
    # assert app.session.is_logged_in_as(username)
    # app.session.logout()
    # sprawdzenie przez soap
    assert app.soap.can_login(username, password)


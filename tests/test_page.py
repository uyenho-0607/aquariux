import time


def test(pages):
    pages.login_page.login("2091004299", "kf5OE!HB48!g")
    pages.home_page.verify_login_succeeded()
    time.sleep(10)

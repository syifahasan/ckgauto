from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = 'input[id="email"]'
        self.password = 'input[id="password"]'
        self.login_btn = 'button[type="submit"]'

    def open(self, base_url: str):
        self.page.goto(base_url)

    def login(self, email: str, password: str):
        self.page.fill(self.email, email)
        self.page.fill(self.password, password)
        self.page.click(self.login_btn)
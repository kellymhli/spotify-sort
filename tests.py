import unittest
from selenium import webdriver

# browser = webdriver.Chrome("./Downloads/chromedriver")
# browser.get("http://localhost:8888")
# assert browser.title == "Homepage"

# logout = browser.find_element_by_id("logout")
# logout.click()

# result = browser.find_element_by_id("login")
# assert result.text == "Login"

class TestApp(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get("http://localhost:8888/")
        self.assertEqual(self.browser.title, "Homepage")
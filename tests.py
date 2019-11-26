import unittest, time, server
from selenium import webdriver

# browser = webdriver.Chrome("./chromedriver")
# browser.get("http://localhost:8888")
# assert browser.title == "Homepage"

# logout = browser.find_element_by_id("logout")
# logout.click()

# result = browser.find_element_by_id("login")
# assert result.text == "Login"

# class TestApp(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome("./chromedriver")

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get("http://localhost:8888/")
#         self.assertEqual(self.browser.title, "Homepage")

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    client = server.app.test_client()

    def test_homepage(self):
        """Assure index returns hompage html."""

        result = self.client.get("/")
        self.assertIn(b"<h1>Spotify Sort</h1>", result.data)

    def test_login(self):
        """Assure login route returns login.html."""

        result = self.client.get("/login")
        self.assertIn(b"<input type='submit' value='Login'>", result.data)

    def test_register_page(self):
        """Assure register route returns register.html"""

        result = self.client.get("/register")
        self.assertIn(b"Spotify Username: <input type=", result.data)
        self.assertIn(b"Confirm Password:", result.data)

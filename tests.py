import unittest, server
from selenium import webdriver


# browser = webdriver.Chrome("chromedriver")
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

###############################################################################
class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    client = server.app.test_client()

    def test_homepage(self):
        """Assure index returns hompage html."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h1>Spotify Sort</h1>", result.data)

    def test_login_page(self):
        """Assure login route returns login.html."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<input type='submit' value='Login'>", result.data)

    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login",
    #                               data={"user_id": "kelly", "password": "music"},
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     print("pass login")

    def test_register_page(self):
        """Assure register route returns register.html"""

        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Spotify Username: <input type=", result.data)
        self.assertIn(b"Confirm Password:", result.data)


class FlaskTestLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """This to do before each test."""

        server.app.config["TESTING"] = True
        server.app.config["SECRET_KEY"] = 'oh-so-secret-key'
        self.client = server.app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = "kelly"
                sess["spotify_id"] = "kalamoing"
                sess["logged_in"] = True

    def test_display_playlists(self):
        """Test playlists page."""
        result = self.client.get("/playlists")
        self.assertEqual(result.status_code, 200)
        print("pl pass")


if __name__ == "__main__":
    """Run tests when tests.py is called."""

    t = TestFlaskRoutes()
    t.test_homepage()
    t.test_login_page()
    # t.test_login()
    t.test_register_page()

    ft = FlaskTestLoggedIn()
    ft.setUp()
    ft.test_display_playlists()

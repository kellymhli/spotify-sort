import unittest, server
from server import app
from selenium import webdriver
from model import User, Playlist, PlaylistTrack, Track, Key, MatchingKey, connect_to_db, db, example_data

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

    def setUp(self):
        """Do before every test."""

        # Get Flask test client
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = 'oh-so-secret-key'
        self.client = app.test_client()

        # Connnect to test db
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and sample data
        db.create_all()
        example_data()

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

    def test_correct_login(self):
        """Assure correct login behavior when valid info is give."""

        result = self.client.post("/login",
                                  data={"user_id": "kels", "password": "wiggle"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Playlist", result.data)

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

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = 'oh-so-secret-key'
        self.client = app.test_client()

        # Connnect to test db
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = "kels"
                sess["spotify_id"] = "kelspot"

    def test_display_playlists(self):
        """Test playlists route displays playlists."""

        result = self.client.get("/playlists")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h1>Playlists</h1>", result.data)
        self.assertIn(b"120</option>", result.data)  # BPM
        self.assertIn(b"Happy</option>", result.data)  # Mood of tracks

    def test_loggedin(self):
        """Test user gets redirected to playlists if already logged in."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 302)
        self.assertIn(b"playlist", result.data)

    def test_logout(self):
        """Test successful logout."""

        result = self.client.get("/logout")
        self.assertEqual(result.status_code, 302)

    def test_playlists(self):
        """Assure playlist page loads with correct data."""

        result = self.client.get("/playlists")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"BPM", result.data)


if __name__ == "__main__":
    """Run tests when tests.py is called."""

    unittest.main()
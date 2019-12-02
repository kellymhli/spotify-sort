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
# Unittests

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
        self.assertIn(b"Mood", result.data)

    def test_get_pl_tracks(self):
        """Assure tracks associated with pl1 and pl2 are displayed."""

        # Playlist 1
        result1 = self.client.get("playlist/pl1")
        self.assertEqual(result1.status_code, 200)
        self.assertIn(b"Track 1", result1.data)
        self.assertIn(b"Track 3", result1.data)
        self.assertNotIn(b"Track 5", result1.data)

        # Playlist 2
        result2 = self.client.get("playlist/pl2")
        self.assertEqual(result2.status_code, 200)
        self.assertIn(b"Track 4", result2.data)
        self.assertIn(b"Track 5", result2.data)
        self.assertNotIn(b"Track 1", result2.data)

    def test_display_tracks(self):
        """Test all tracks shown."""

        result = self.client.get("/tracks")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Track 1", result.data)
        self.assertIn(b"Track 5", result.data)

    # def test_sort_tracks(self):
    #     """Test tracks of selected playlist display in sort-playlists route."""

    #     result1 = self.client.get("/sort-playlists",
    #                               data={("playlist", "pl1")})
    #     self.assertEqual(result1.status_code, 200)
    #     self.assertIn(b"Track 2", result1.data)
    #     self.assertNotIn(b"Track 4", result1.data)

    #     result2 = self.client.get("/sort-playlists",
    #                               data={("playlist", "pl1"), ("playlist", "pl2")})
    #     self.assertEqual(result2.status_code, 200)
    #     self.assertIn(b"Track 2", result2.data)
    #     self.assertIn(b"Track 4", result2.data)

if __name__ == "__main__":
    """Run tests when tests.py is called."""

    unittest.main()
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension

import model

app = Flask(__name__)
app.secret_key = "ILIKEWIGGLINGTOMUSIC"

# Raise error when an undefined variable is used in Jinja2
# rather than failing silently
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":

    # Needs to be true upon invoking DebugToolbarExtension
    app.debug = True 
    # Make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug 

    model.connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=8888, host="0.0.0.0")
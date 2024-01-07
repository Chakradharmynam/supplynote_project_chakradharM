from flask import Flask, redirect
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import logout_user

app = Flask(__name__)
blueprint = make_google_blueprint()
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/logout")
def logout():
    token = blueprint.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.ok, resp.text
    logout_user()        # Delete Flask-Login's session cookie
    del blueprint.token  # Delete OAuth token from storage
    return redirect(somewhere)
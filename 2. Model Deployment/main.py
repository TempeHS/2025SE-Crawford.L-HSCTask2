from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
    session,
    g,
    Response,
)
from flask_session import Session
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import os
from flask_wtf.csrf import generate_csrf
from flask_talisman import Talisman, ALLOW_FROM

import pyfiles.register_manager as rm
import pyfiles.forms as forms

app_log = logging.getLogger(__name__)
file_handler = logging.FileHandler("main_security_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
app_log.addHandler(file_handler)
app_log.propagate = False

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"6HlQfWhu03PttohW;apl"

# Flask-Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = b"6HlQfWhu03PttohW;apl"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour
Session(app)

# Flask-Talisman configuration
csp = {
    "default-src": ["'self'"],
    "style-src": ["'self'", "https://cdn.jsdelivr.net/"],
    "script-src": [
        "'self'",
        "https://cdn.jsdelivr.net/",
        "'nonce-{nonce}'",
        "'strict-dynamic'",
        "'unsafe-inline'",
    ],
    "img-src": ["'self'", "data:"],
    "media-src": ["'self'"],
    "font-src": ["'self'", "data:"],
    "connect-src": ["'self'"],
    "object-src": ["'self'"],
    "worker-src": ["'self'"],
    "frame-src": ["'none'"],
    "form-action": ["'self'"],
    "manifest-src": ["'self'"],
    "base-uri": ["'self'"],
}

talisman = Talisman(
    app, content_security_policy=csp, content_security_policy_nonce_in=["script-src"]
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.context_processor
def inject_nonce():
    return dict(csp_nonce=talisman._get_nonce())


@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
    csp=csp,
)
def index():
    app_log.debug(f"Session state at /: {session}")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        response, status_code = rm.create_user(username, email, password)
        if status_code == 201:

            response_json = response.get_json()
            qr_code_data = response_json.get("qr_code_data")
            return render_template(
                "register/register_success.html", qr_code_data=qr_code_data
            )
        return response, status_code
    return render_template("register/register.html", form=forms.RegistrationForm())


@app.route("/register_success", methods=["GET"])
def register_success():
    return "Registration successful"


@app.route("/login", methods=["GET", "POST"])
@csp_header(
    csp=csp,
)
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if rm.checkPW(username, password):
            session.clear()  # Clear the old session
            session["username"] = username  # Set the new session data
            csrf_token = generate_csrf()  # Generate the CSRF token
            app_log.debug(f"CSRF token after login: {csrf_token}")
            app_log.debug(f"Session state after login: {session}")
            return redirect("/login_success", 302)
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template("register/login.html", form=form)


@app.route("/login_success", methods=["GET"])
def login_success():
    app_log.debug(f"Session state at /login_success: {session}")
    if "username" in session:
        return f"Login successful, welcome {session['username']}.  Return to <a href='/'>Home</a>"
    return redirect("/login")


@app.route("/get-session", methods=["GET"])
@csp_header(
    csp=csp,
)
def get_session():
    app_log.debug(f"Session state at /get_session: {session}")
    if "username" in session:
        user_details = {
            "username": session["username"],
            # Add other session details if available
        }
        session_data = dict(session)  # Convert session to a dictionary
        return jsonify({"session_state": session_data, "user_details": user_details})
    return jsonify({"error": "No session found"}), 404


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    app_log.debug(f"Session state after logout: {session}")
    return redirect("/")


@app.route("/change-password", methods=["GET", "POST"])
@csp_header(
    csp=csp,
)
def change_password():
    form = forms.chPWForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        new_password = form.password.data

        response, status_code = rm.changePW(username, email, new_password)
        if status_code == 200:
            session.clear()
            session["username"] = username
            csrf_token = generate_csrf()
            app_log.debug(f"CSRF token after password change: {csrf_token}")
            app_log.debug(f"Session state after password change: {session}")
            return redirect("/change_password_success", 302)
        else:
            return jsonify(response), status_code

    return render_template("register/change_password.html", form=form)


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    username = request.form.get("username")
    otp = request.form.get("otp")
    response, status_code = rm.verify_otp(username, otp)
    return response, status_code


@app.route("/all-posts", methods=["GET"])
@csp_header(
    csp=csp,
)
def all_posts():
    response = requests.post("http://127.0.0.1:4000/all-posts")
    status_code = response.status_code
    if status_code == 200:

        return jsonify(response.json()), status_code
    else:
        return f"Code {status_code}: {response}"


@app.route("/create-post", methods=["GET", "POST"])
@csp_header(
    csp=csp,
)
def create_post():
    uuid = rm.get_uuid(session.get("username"))
    form = forms.createPostForm()
    if form.validate_on_submit():
        developer = form.developer.data
        project = form.project.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        diary_time = form.diary_time.data
        time_worked = form.time_worked.data
        repo = form.repo.data
        dev_notes = form.dev_notes.data

        response = requests.post(
            "http://127.0.0.1:4000/add-post",
            json={
                "uuid": uuid,
                "developer": developer,
                "project": project,
                "start_time": start_time,
                "end_time": end_time,
                "diary_time": diary_time,
                "time_worked": time_worked,
                "repo": repo,
                "dev_notes": dev_notes,
            },
        )
        status_code = response.status_code
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = {"error": "Invalid response from server"}

        if status_code == 200:
            return jsonify(response_json), status_code
        else:
            return jsonify(response_json), status_code

    return render_template("posts/create_post.html", form=form)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

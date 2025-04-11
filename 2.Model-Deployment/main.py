import logging
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
)
import requests
from flask_csp.csp import csp_header
from dotenv import load_dotenv
import os
import base64
import pyfiles.predict as pred

load_dotenv()

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="main_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)

app.secret_key = os.urandom(24)


# Flask-Talisman configuration
csp = {
    "default-src": "'self'",
    "style-src": "'self' https://cdn.jsdelivr.net/",
    "script-src": "'self' https://cdn.jsdelivr.net/ https://zany-potato-9r5w9rrrqx5c4x5-5000.app.github.dev/static/",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self' data:",
    "connect-src": "'self'",
    "object-src": "'none'",
    "worker-src": "'self'",
    "frame-src": "'none'",
    "form-action": "'self'",
    "manifest-src": "'self'",
    "base-uri": "'self'",
}


@app.context_processor
def inject_nonce():
    """
    Injects the CSP nonce into the template context for use in inline scripts.
    Returns:
            dict: A dictionary containing the CSP nonce.
    This nonce is used to allow specific inline scripts to be executed
    while still maintaining a secure Content Security Policy (CSP).
    """
    # Safely retrieve the CSP nonce from the request object
    csp_nonce = getattr(request, "csp_nonce", "")
    return dict(csp_nonce=csp_nonce)


@app.route("/index.html", methods=["GET"])
def root():
    """
    Redirects the root URL ("/") to the index page ("/index.html").
    This route handles GET requests to the root URL and performs a redirect.
    """

    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
    csp=csp,
)
def index():
    """
    Renders the index page.
    """
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
@csp_header(
    csp=csp,
)
def predict():
    """
    Handles the prediction request.
    This route accepts POST requests with either form data or JSON data.
    """
    if request.form:
        # Handle form data
        data = {
            "air_temp": request.form.get("air_temp"),
            "dewpt": request.form.get("dewpt"),
            "rel_hum": request.form.get("rel_hum"),
            "press": request.form.get("press"),
            "apparent_t": request.form.get("apparent_t"),
        }
    elif request.is_json:
        # Handle JSON data
        data = request.json
    else:
        return jsonify({"status": "error", "message": "Unsupported content type"}), 400

    app_log.debug("Received data: %s", data)

    prediction = pred.predict(data)
    app_log.debug("Prediction result: %s", prediction)
    # Log the prediction result

    # Validate and process the data
    if not data:
        return jsonify({"status": "error", "message": "Empty data received"}), 400

    response_data = {
        "status": "success",
        "data": data,
        "prediction": prediction,
    }
    app_log.debug("Response data: %s", response_data)

    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

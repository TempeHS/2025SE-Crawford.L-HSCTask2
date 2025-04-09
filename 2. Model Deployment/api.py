from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import pyfiles.post_manager as pm
import pyfiles.register_manager as rm
from dotenv import load_dotenv

# Configure logging for api.py
api_log = logging.getLogger(__name__)
file_handler = logging.FileHandler("api_security_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
api_log.addHandler(file_handler)
api_log.propagate = False

api = Flask(__name__)
api.secret_key = r"nEksrUMh4vnYXa9I52U7uUs4TX2mA1yk"  # Ensure you have a secret key for session management
CORS(api)
limiter = Limiter(
    app=api,
    key_func=get_remote_address,
    default_limits=["1 per second", "15 per minute"],
    storage_uri="memory://",
)


@api.before_request
def log_request_info():
    api_log.debug(f"Request Headers: {request.headers}")
    api_log.debug(f"Request Body: {request.get_data()}")


def get_request_data():
    if request.content_type == "application/json":
        return request.get_json()
    elif request.content_type == "application/x-www-form-urlencoded":
        return request.form.to_dict()
    else:
        return {}


@api.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized Access!"}), 401


@api.route("/api", methods=["POST"])
def get_data():
    data = get_request_data()
    api_log.info(f"Received data: {data}")
    return jsonify(data), 200


@api.route("/all-posts", methods=["POST"])

def get_all_posts():
    api_log.info("Getting all posts")
    all = pm.all_posts()
    api_log.info(f"Posts: {all}")
    return jsonify(all), 200


@api.route("/add-post", methods=["POST"])
def add_post():
    data = get_request_data()
    uuid = data.get("uuid")
    api_log.info(f"Received data: {data}")
    result, status_code = pm.add_post(data, uuid)
    return jsonify(result), status_code


if __name__ == "__main__":
    api.run(debug=False, host="0.0.0.0", port=4000)

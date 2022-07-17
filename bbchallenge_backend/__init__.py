from os import getenv

from flask import Flask
from flask_cors import CORS


from bbchallenge_backend.ping import ping_bp
from bbchallenge_backend.machines import machines_bp
from bbchallenge_backend.metrics import metrics_bp


import os, sys


def create_app(config={}):

    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

    secret_key_file_path = os.path.join(os.getcwd(), "secret_key.config.py")

    if not os.path.isfile(secret_key_file_path):
        try:
            with open(secret_key_file_path, "w") as f:
                f.write(f"SECRET_KEY = {os.urandom(12)}")
        except OSError as e:
            print(
                f"Cannot create `{secret_key_file_path}` with flask's secret key: {e}. Please refer to https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask"
            )
            sys.exit(-1)

    app.config.from_pyfile(os.path.join(os.getcwd(), "secret_key.config.py"))

    # if "TESTING" not in config:
    #     config["TESTING"] = False

    # if getenv("ENV") is not None:
    #     config["ENV"] = getenv("ENV")

    # app.config.update(config)

    # app.mongo = PyMongo(app)

    # # Email API
    # if not "POSTMARK_API_KEY" in app.config:
    #     print("No Postmark key was given. Abort.")
    #     sys.exit(-1)

    # app.postmark = PostmarkClient(server_token=app.config["POSTMARK_API_KEY"])

    app.register_blueprint(ping_bp)
    app.register_blueprint(machines_bp)
    app.register_blueprint(metrics_bp)
    CORS(app, supports_credentials=True)
    return app


app = create_app()

# This allows the client to read the Content-Disposition header
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response


# @app.before_request
# def check_user_is_logged():
#     if request.method == "OPTIONS":
#         return

#     print(request, request.endpoint, session)
#     if request.endpoint == "auth.login":
#         return
#     if "email" not in session:
#         return "Not Authorized", 403

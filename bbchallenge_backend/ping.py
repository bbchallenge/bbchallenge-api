from flask import Blueprint


ping_bp = Blueprint("ping_bp", __name__)


@ping_bp.route("/ping", methods=["GET"])
def ping():
    return "pong"

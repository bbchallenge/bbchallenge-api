from flask import Blueprint, jsonify, current_app
from bbchallenge_backend.utils import get_undecided_db_size

metrics_bp = Blueprint("metrics_bp", __name__)


@metrics_bp.route("/metrics")
def random_machine():

    total_undecided = get_undecided_db_size()

    to_ret = {
        "total": current_app.config["DB_SIZE"],
        "total_undecided": total_undecided,
    }

    return jsonify(to_ret), 200

from crypt import methods
import random
from flask import Blueprint, jsonify, request, current_app
from bbchallenge_backend.utils import (
    REDIS_DB_UNDECIDED,
    REDIS_DB_UNDECIDED_HEURISTICS,
    DB_SIZE,
)

metrics_bp = Blueprint("metrics_bp", __name__)


@metrics_bp.route("/metrics")
def random_machine():

    current_app.r.select(REDIS_DB_UNDECIDED)
    total_undecided = current_app.r.dbsize()
    current_app.r.select(REDIS_DB_UNDECIDED_HEURISTICS)
    total_undecided_with_heuristics = current_app.r.dbsize()

    to_ret = {
        "total": DB_SIZE,
        "total_undecided": total_undecided,
        "total_undecided_with_heuristcs": total_undecided_with_heuristics,
    }

    return jsonify(to_ret), 200

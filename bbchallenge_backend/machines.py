from crypt import methods
import random
from flask import Blueprint, jsonify, request, current_app
from bbchallenge_backend.utils import (
    get_machine_i,
    get_machine_i_status,
    get_random_machine_in_db,
    get_machine_code,
    REDIS_DB_UNDECIDED,
    REDIS_DB_UNDECIDED_HEURISTICS,
    DB_SIZE,
)

machines_bp = Blueprint("machines_bp", __name__)


@machines_bp.route("/machine/random", methods=["GET", "POST"])
def random_machine():

    req = request.json

    if req is None or not "type" in req:
        if req is None:
            req = {}
        req["type"] = "all_undecided_apply_heuristics"

    if req["type"] == "all":
        machine_id = random.randint(0, DB_SIZE - 1)
    elif req["type"] == "all_undecided":
        try:
            machine_id = get_random_machine_in_db(REDIS_DB_UNDECIDED)
        except ValueError as e:
            return jsonify({"error": e}), 400
    else:
        try:
            machine_id = get_random_machine_in_db(REDIS_DB_UNDECIDED_HEURISTICS)
        except ValueError as e:
            return jsonify({"error": e}), 400

    return machine_i(machine_id)


@machines_bp.route("/machine/<int:machine_id>")
def machine_i(machine_id):
    try:
        machine_code = get_machine_code(get_machine_i(machine_id))
        to_ret = {"machine_id": machine_id, "machine_code": machine_code}
        to_ret.update(get_machine_i_status(machine_id))
    except ValueError as e:
        return jsonify({"error": e}), 400

    return jsonify(to_ret), 200

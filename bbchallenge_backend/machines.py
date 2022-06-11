import os
import random
from flask import Blueprint, jsonify, request
from bbchallenge_backend.utils import (
    get_machine_i,
    get_machine_i_status,
    get_random_machine_in_db,
    get_machine_code,
    REDIS_DB_UNDECIDED,
    REDIS_DB_UNDECIDED_HEURISTICS,
    DB_SIZE,
)

# https://github.com/tcosmo/dichoseek
from dichoseek import dichoseek

machines_bp = Blueprint("machines_bp", __name__)


@machines_bp.route("/machine/<int:machine_id>/decider")
def machine_decider(machine_id):
    to_ret = {"decider_file": None}
    indexes_base_path = "indexes/bb5_decided_indexes"
    for elem in os.listdir(indexes_base_path):
        elem_path = os.path.join(indexes_base_path, elem)
        if os.path.isfile(elem_path):
            if dichoseek(elem_path, machine_id):
                to_ret["decider_file"] = elem
                break

    return jsonify(to_ret), 200


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

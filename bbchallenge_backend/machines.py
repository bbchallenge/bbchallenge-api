import os
import random
from flask import Blueprint, current_app, jsonify, request
from bbchallenge_backend.utils import (
    get_machine_i,
    get_machine_i_status,
    get_undecided_db_size,
    get_machine_code,
    _get_map,
)

# https://github.com/tcosmo/dichoseek
from dichoseek import dichoseek

machines_bp = Blueprint("machines_bp", __name__)


@machines_bp.route("/machine/<int:machine_id>/decider")
def machine_decider(machine_id):
    to_ret = {"decider_file": None}
    indexes_base_path = current_app.config["DB_PATH_DECIDED"]
    for elem in os.listdir(indexes_base_path):
        if not "run" in elem:
            continue
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

    if req["type"] == "all_undecided":
        random_machine_id_index = random.randint(0, get_undecided_db_size() - 1)
        f = _get_map(current_app.config["DB_PATH_UNDECIDED"])
        f.seek(4 * random_machine_id_index)
        machine_id = int.from_bytes(f.read(4), byteorder="big")
    else:
        machine_id = random.randint(0, current_app.config["DB_SIZE"] - 1)

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

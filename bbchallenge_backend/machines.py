import os
import random
from flask import Blueprint, current_app, jsonify, request
from bbchallenge_backend.utils import (
    get_machine_i,
    get_machine_i_status,
    get_undecided_db_size,
    get_machine_code,
    get_nth_machine_id_in_index_file,
    dichoseek_mmap,
)


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
            if dichoseek_mmap(elem_path, machine_id):
                to_ret["decider_file"] = elem
                break

    return jsonify(to_ret), 200


@machines_bp.route("/machine/random", methods=["GET"])
def random_machine():
    random_type = request.args.get("type")

    if random_type is None:
        random_type = "all_undecided"

    if random_type == "all_undecided":
        random_machine_id_index = random.randint(0, get_undecided_db_size() - 1)
        machine_id = get_nth_machine_id_in_index_file(
            current_app.config["DB_PATH_UNDECIDED"], random_machine_id_index
        )

    else:
        machine_id = random.randint(0, current_app.config["DB_SIZE"] - 1)

    print(machine_id)
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

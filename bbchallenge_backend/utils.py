import os
from flask import current_app

# https://github.com/tcosmo/dichoseek
from dichoseek import dichoseek


def is_valid_machine_index(machine_id):
    return machine_id >= 0 and machine_id < current_app.config["DB_SIZE"]


def get_undecided_db_size():
    return os.stat(current_app.config["DB_PATH_UNDECIDED"]).st_size // 4


def get_machine_code(machine_bytes):
    to_ret = ""
    for i, b in enumerate(machine_bytes):
        if i % 3 == 0:
            if machine_bytes[i + 2] == 0:
                to_ret += "-"
                continue
            if b == 0:
                to_ret += "0"
            else:
                to_ret += "1"
        elif i % 3 == 1:
            if machine_bytes[i + 1] == 0:
                to_ret += "-"
                continue
            if b == 0:
                to_ret += "R"
            else:
                to_ret += "L"
        else:
            if b == 0:
                to_ret += "-"
            else:
                to_ret += chr(ord("A") + b - 1)
    return to_ret


def get_machine_i(i, db_has_header=True):
    if not is_valid_machine_index(i):
        raise ValueError(
            "Machine IDs must be number between 0 and 88,664,064 excluded."
        )

    with open(current_app.config["DB_PATH"], "rb") as f:
        c = 1 if db_has_header else 0
        f.seek(30 * (i + c))
        bytes_ = f.read(30)

        return bytes_


def get_machine_i_status(machine_id):
    if not is_valid_machine_index(machine_id):
        raise ValueError(
            "Machine IDs must be number between 0 and 88,664,064 excluded."
        )

    is_undecided = dichoseek(
        current_app.config["DB_PATH_UNDECIDED"], machine_id
    )

    if is_undecided:
        return {"status": "undecided"}

    return {"status": "decided"}

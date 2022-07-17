import os
import mmap
from flask import current_app

# https://github.com/tcosmo/dichoseek
from dichoseek import dichoseek

map_mmaps = {}

def _get_map(path):
    if path not in map_mmaps:
        with open(path, "rb") as f:
            map_mmaps[path] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    return map_mmaps[path]

def is_valid_machine_index(machine_id):
    return machine_id >= 0 and machine_id < current_app.config["DB_SIZE"]


def get_undecided_db_size():
    return len(_get_map(current_app.config["DB_PATH_UNDECIDED"])) // 4


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

    db_map = _get_map(current_app.config["DB_PATH"])
    c = 1 if db_has_header else 0
    offs = 30 * (i + c)
    return db_map[offs:offs+30]


def get_machine_i_status(machine_id):
    if not is_valid_machine_index(machine_id):
        raise ValueError(
            "Machine IDs must be number between 0 and 88,664,064 excluded."
        )

    db_undecided_map = _get_map(current_app.config["DB_PATH_UNDECIDED"])
    is_undecided = dichoseek(db_undecided_map, machine_id)

    if is_undecided:
        return {"status": "undecided"}

    return {"status": "decided"}

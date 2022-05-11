import base64
from flask import current_app


DB_SIZE = 88664064

REDIS_DB_UNDECIDED = 0
REDIS_DB_UNDECIDED_HEURISTICS = 1
REDIS_DB_HIGHLITS = 2


def is_valid_machine_index(machine_id):
    return machine_id >= 0 and machine_id < DB_SIZE


def get_random_machine_in_db(redis_db):
    current_app.r.select(redis_db)
    machine_id = current_app.r.randomkey()
    if machine_id is None:
        raise ValueError(f"no machines in redis DB{redis_db}.")
    return int(machine_id.decode())


def get_machine_code(machine_bytes):
    to_ret = ""
    for i, b in enumerate(machine_bytes):
        if i%3 == 0:
            if machine_bytes[i+2] == 0:
                to_ret += "-"
                continue
            if b == 0:
                to_ret += "0"
            else:
                to_ret += "1"
        elif i%3 == 1:
            if machine_bytes[i+1] == 0:
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
                to_ret += chr(ord("A")+b-1)
    return to_ret

def get_machine_i(i, db_has_header=True, b64=False):
    if not is_valid_machine_index(i):
        raise ValueError(
            "Machine IDs must be number between 0 and 88,664,064 excluded."
        )

    with open(current_app.config["DB_PATH"], "rb") as f:
        c = 1 if db_has_header else 0
        f.seek(30 * (i + c))
        bytes_ = f.read(30)
        if not b64:
            return bytes_
        else:
            the_string = ""
            for a in bytes_:
                the_string += chr(a)
            return (
                (("m".encode() + base64.urlsafe_b64encode(the_string.encode())))
                .decode()
                .rstrip("=")
            )


def get_machine_i_status(i):
    if not is_valid_machine_index(i):
        raise ValueError(
            "Machine IDs must be number between 0 and 88,664,064 excluded."
        )

    current_app.r.select(REDIS_DB_UNDECIDED)
    is_undecided = current_app.r.exists(i)

    current_app.r.select(REDIS_DB_UNDECIDED_HEURISTICS)
    is_undecided_with_heuristics = current_app.r.exists(i)

    if is_undecided_with_heuristics:
        return {"status": "undecided"}
    elif is_undecided:
        return {"status": "heuristic"}
    else:
        return {"status": "decided"}

from crypt import methods
import random
from flask import Blueprint, jsonify, request, current_app
from bbchallenge_backend.utils import (
    REDIS_DB_UNDECIDED,
    REDIS_DB_UNDECIDED_HEURISTICS,
    REDIS_DB_HIGHLITS,
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


@metrics_bp.route("/highlighted")
def highlighted():
    current_app.r.select(REDIS_DB_HIGHLITS)

    highlighted_list = list(
        map(lambda x: x.decode(), current_app.r.lrange("highlighted", 0, -1))
    )

    highlighted_undecided = []
    highlighted_halt = []

    for h in highlighted_list:
        sp = h.split(";")
        title = None
        link = sp[0]
        b64 = None
        ID = None

        if len(sp) > 1:
            title = sp[0]
            link = sp[1]

        if link[0] == "m":
            b64 = link.split("&")[0]
        else:
            ID = link.split("&")[0]

        dict_do_add = {}
        if b64 is not None:
            dict_do_add["b64"] = b64
        if ID is not None:
            dict_do_add["machine_id"] = ID

        dict_do_add.update({"link": link})
        if title is not None:
            dict_do_add.update({"title": title})
            if "halter" in title:
                highlighted_halt.append(dict_do_add)
            else:
                highlighted_undecided.append(dict_do_add)
        else:
            highlighted_undecided.append(dict_do_add)

    return {
        "highlighted_undecided": tuple(highlighted_undecided),
        "highlighted_halt": tuple(highlighted_halt),
    }

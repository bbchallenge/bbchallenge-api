from typing import Union


class TMNormalizationError(Exception):
    pass


def index_of(e, l):
    # print(e,l)
    for i, a in enumerate(l):
        if a == e:
            return i


def normalize_machine(machine_code: str) -> Union[None, str]:
    """Returns the normalised machine. Only for 5-state 2-symbol machines
    that write a 1 in their first transition.

    Normalization consists in:

    1. Symmetrise L/R so that first transition goes to R
    2. Re-order states in the order that they are visited

    """

    if len(machine_code) != 34:
        raise TMNormalizationError(
            f"`{machine_code}` is not a 5-state 2-symbol machine"
        )

    if machine_code[0] != "1":
        raise TMNormalizationError(
            f"The first transition of `{machine_code}` does not write a 1"
        )

    # 1. Symmetrise machine
    if machine_code[1] != "R":
        machine_code = machine_code.replace("R", "@")
        machine_code = machine_code.replace("L", "R")
        machine_code = machine_code.replace("@", "L")

    # 2. Reorder machine
    # Run the machine for BB(4) = 107 steps
    machine_code = machine_code.replace("_", "")
    tape = {0: 0}
    head_pos = 0
    curr_state = 0
    curr_time = 0
    state_first_seen = []
    while curr_time < 107 + 10:
        if curr_state not in state_first_seen:
            state_first_seen.append(curr_state)
        if head_pos not in tape:
            tape[head_pos] = 0
        curr_read = tape[head_pos]
        write, move, _goto = machine_code[
            curr_state * 6 + curr_read * 3 : curr_state * 6 + curr_read * 3 + 3
        ]
        if _goto == "-":
            return None
        tape[head_pos] = 0 if write == "0" else 1
        head_pos += 1 if move == "R" else -1
        curr_state = ord(_goto) - ord("A")
        curr_time += 1

    if len(state_first_seen) != 5:
        return None

    new_machine_code = ""
    for state in state_first_seen:
        for i in range(6):
            e = machine_code[state * 6 + i]
            if i % 3 != 2 or e == "-":
                new_machine_code += e
            else:
                new_machine_code += chr(
                    ord("A") + index_of(ord(e) - ord("A"), state_first_seen)
                )

    separated_new_machine_code = ""
    for i, e in enumerate(new_machine_code):
        separated_new_machine_code += e
        if i % 6 == 5 and i + 1 != len(new_machine_code):
            separated_new_machine_code += "_"

    return separated_new_machine_code

def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1-R4: combinational output based on current state
    # R5: synchronous active high reset -> state A
    # R6-R9: state transitions on posedge
    # Initial state assumed A (global uncertainty)
    state = 0  # A
    out = 0
    results = []
    for v in vectors:
        # Mid changes occur AFTER sampling, before other edge, carried to next row.
        # We process: sample current state's output, then apply posedge transition.
        # R1: state A -> out 0
        # R2: state B -> out 0
        # R3: state C -> out 0
        # R4: state D -> out 1
        if state == 0:
            out = 0  # R1
        elif state == 1:
            out = 0  # R2
        elif state == 2:
            out = 0  # R3
        else:
            out = 1  # R4
        results.append({"out": out})
        # Posedge transition (R5-R9)
        reset = v.get("reset", 0)
        inp = v.get("in", 0)
        if reset == 1:
            state = 0  # R5
        else:
            if state == 0:
                state = 0 if inp == 0 else 1  # R6
            elif state == 1:
                state = 2 if inp == 0 else 1  # R7
            elif state == 2:
                state = 0 if inp == 0 else 3  # R8
            else:
                state = 2 if inp == 0 else 1  # R9
    return results

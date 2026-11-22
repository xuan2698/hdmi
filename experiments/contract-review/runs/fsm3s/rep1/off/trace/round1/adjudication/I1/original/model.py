def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; choose A)
    out = 0
    results = []

    for vec in vectors:
        # R_RESET / R_TRANS: sample inputs at posedge
        reset = vec.get('reset', 0)
        inp = vec.get('in', 0)

        # R_RESET: synchronous active high reset -> state A (priority 0)
        if reset == 1:
            state = A
        else:
            # R_TRANS: next state determined by table
            if state == A:
                state = A if inp == 0 else B
            elif state == B:
                state = C if inp == 0 else B
            elif state == C:
                state = A if inp == 0 else D
            elif state == D:
                state = C if inp == 0 else B

        # R_A / R_B / R_C / R_D: combinational output based on current state
        if state == A:
            out = 0  # R_A
        elif state == B:
            out = 0  # R_B
        elif state == C:
            out = 0  # R_C
        elif state == D:
            out = 1  # R_D

        results.append({'out': out & 1})

    return results

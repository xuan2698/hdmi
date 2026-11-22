def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; use A)
    out = 0
    results = []

    for vec in vectors:
        # R_RESET: synchronous active high reset -> state A (posedge, next_cycle)
        # R_TRANS: next state determined by table on posedge when reset == 0
        # R_A/R_B/R_C/R_D: combinational output based on current state (same_cycle)
        # Mid changes occur AFTER sampling, before other edge, carried to next row.
        # We sample inputs at posedge; mid changes are applied after sampling.
        reset = vec.get('reset', 0)
        inp = vec.get('in', 0)

        # Combinational output for current state (R_A, R_B, R_C, R_D)
        if state == A:
            out = 0  # R_A
        elif state == B:
            out = 0  # R_B
        elif state == C:
            out = 0  # R_C
        elif state == D:
            out = 1  # R_D

        results.append({'out': out & 1})

        # Posedge update: compute next state
        if reset == 1:
            next_state = A  # R_RESET
        else:
            # R_TRANS: transition table
            if state == A:
                next_state = A if inp == 0 else B
            elif state == B:
                next_state = C if inp == 0 else B
            elif state == C:
                next_state = A if inp == 0 else D
            elif state == D:
                next_state = C if inp == 0 else B
            else:
                next_state = A

        state = next_state

    return results

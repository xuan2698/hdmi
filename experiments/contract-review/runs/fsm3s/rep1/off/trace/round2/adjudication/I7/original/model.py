def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; use A)
    out = 0
    results = []

    for vec in vectors:
        # R_RESET: synchronous active high reset -> state A (priority 0)
        # R_TRANS: next state determined by table on posedge when reset == 0
        # Sampling happens at posedge; mid changes occur after sampling.
        # We model: apply current inputs to compute next state, then output
        # reflects the state AFTER the edge (Moore output, same_cycle visible
        # means output corresponds to the state reached at this edge).

        reset = vec.get('reset', 0)
        inp = vec.get('in', 0)

        # Compute next state based on current state and inputs (posedge update)
        if reset == 1:
            # R_RESET
            next_state = A
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

        # R_A, R_B, R_C, R_D: combinational output based on state (same_cycle)
        if state == A:
            out = 0  # R_A
        elif state == B:
            out = 0  # R_B
        elif state == C:
            out = 0  # R_C
        elif state == D:
            out = 1  # R_D
        else:
            out = 0

        results.append({'out': out & 0x1})

    return results

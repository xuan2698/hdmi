def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; use reset state A)
    out = 0
    results = []
    for vec in vectors:
        # R_RESET: synchronous active high reset -> state A, out 0 (visible next cycle)
        # R_A/R_B/R_C/R_D: combinational output based on current state
        # R_TRANS: next state determined by table on posedge when reset == 0
        # Sample inputs (driven before sampled edge)
        rst = vec.get('reset', 0)
        inp = vec.get('in', 0)
        # Compute output from current state (combinational, same cycle)
        if state == A:
            out = 0  # R_A
        elif state == B:
            out = 0  # R_B
        elif state == C:
            out = 0  # R_C
        elif state == D:
            out = 1  # R_D
        results.append({'out': out & 1})
        # Compute next state on posedge
        if rst == 1:
            state = A  # R_RESET priority 0
        else:
            # R_TRANS priority 2
            if state == A:
                state = A if inp == 0 else B
            elif state == B:
                state = C if inp == 0 else B
            elif state == C:
                state = A if inp == 0 else D
            elif state == D:
                state = C if inp == 0 else B
        # Mid changes occur AFTER sampling, before other edge, carried to next row.
        # Since vectors provide inputs per row, mid changes are already reflected
        # in the next row's inputs; nothing extra to do here.
    return results

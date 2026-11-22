def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified, but reset will handle)
    out = 0
    results = []

    for vec in vectors:
        # R_RESET: synchronous active high reset -> state A, out 0 (visible next cycle)
        # R_A/R_B/R_C/R_D: combinational output based on current state
        # R_TRANS: next state determined by table on posedge when reset == 0

        # Determine current output combinationally from current state
        if state == A:
            out = 0  # R_A
        elif state == B:
            out = 0  # R_B
        elif state == C:
            out = 0  # R_C
        elif state == D:
            out = 1  # R_D

        # Sample inputs (driven before sampled edge)
        r = vec.get('reset', 0)
        i = vec.get('in', 0)

        # Record output for this cycle (combinational, same_cycle visibility)
        results.append({'out': out & 1})

        # Compute next state on posedge
        if r == 1:
            # R_RESET: synchronous reset to A
            state = A
        else:
            # R_TRANS: transition table
            if state == A:
                state = A if i == 0 else B
            elif state == B:
                state = C if i == 0 else B
            elif state == C:
                state = A if i == 0 else D
            elif state == D:
                state = C if i == 0 else B

        # Mid input changes occur AFTER sampling, before other edge,
        # carried to start of next row. Since we read vec each iteration,
        # mid changes are naturally applied at the start of the next row.

    return results

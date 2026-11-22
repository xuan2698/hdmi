def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up unspecified; start at A
    out = 0
    results = []

    for vec in vectors:
        # R1/R2: combinational output based on current state (visible same cycle)
        if state == D:
            out = 1  # R2
        else:
            out = 0  # R1

        # Sample inputs at posedge
        in_val = vec.get('in', 0)
        reset_val = vec.get('reset', 0)

        # R3: synchronous active-high reset -> next state A, out 0
        if reset_val == 1:
            state = A
            out = 0
        else:
            # R4-R7: state transitions
            if state == A:
                state = B if in_val == 1 else A  # R4
            elif state == B:
                state = B if in_val == 1 else C  # R5
            elif state == C:
                state = D if in_val == 1 else A  # R6
            elif state == D:
                state = B if in_val == 1 else C  # R7

        # Output visible for this row is the combinational output before edge
        # (Moore output depends on current state, sampled same cycle)
        # Recompute output for the row based on state BEFORE the edge
        # We already computed out above based on pre-edge state.
        results.append({'out': out & 0x1})

    return results

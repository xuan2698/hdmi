def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    # R3: reset is synchronous active high; output during reset is don't-care.
    # We model state as unknown before first reset release (global uncertainty),
    # but since output during reset is don't-care, we output 0 during reset.
    # Initial state before first reset release: unspecified -> we use A as a
    # concrete placeholder but mark outputs as don't-care (we output 0).
    state = A
    out = 0
    results = []
    for vec in vectors:
        # Each row's values are driven before the sampled edge.
        # Mid changes occur AFTER sampling, before the other edge, and are
        # carried to the start of the next row. We process the row's inputs
        # as the values present at the sampled posedge.
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)
        # R3: synchronous reset -> state A, output don't-care (we use 0)
        if rst == 1:
            state = A
            out = 0  # R3: output during reset is don't-care; concrete 0
        else:
            # R1/R2: combinational output based on current state
            if state == D:
                out = 1  # R2
            else:
                out = 0  # R1 (A, B, C)
            # R4-R7: next state transitions on posedge
            if state == A:
                # R4
                state = B if inp == 1 else A
            elif state == B:
                # R5
                state = B if inp == 1 else C
            elif state == C:
                # R6
                state = D if inp == 1 else A
            elif state == D:
                # R7
                state = B if inp == 1 else C
        results.append({'out': out & 1})
    return results

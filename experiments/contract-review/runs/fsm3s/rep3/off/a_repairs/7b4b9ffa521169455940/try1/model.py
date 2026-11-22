def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; use A)
    out = 0
    results = []
    for vec in vectors:
        # R1/R2: combinational output based on current state (visible same cycle)
        if state == D:
            out = 1  # R2
        else:
            out = 0  # R1
        # Record output for this row (sampled before posedge transition)
        results.append({"out": out})
        # R3/R4/R5/R6/R7: posedge transition
        if vec["reset"] == 1:
            state = A  # R3
        else:
            if state == A:
                state = B if vec["in"] == 1 else A  # R4
            elif state == B:
                state = C if vec["in"] == 0 else B  # R5
            elif state == C:
                state = D if vec["in"] == 1 else A  # R6
            elif state == D:
                state = C if vec["in"] == 0 else B  # R7
    return results

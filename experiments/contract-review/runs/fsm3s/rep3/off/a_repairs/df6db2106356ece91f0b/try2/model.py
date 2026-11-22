def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; choose A)
    out = 0
    results = []
    for vec in vectors:
        # R1/R2: combinational output based on current state (visible same cycle)
        if state == D:
            out = 1  # R2
        else:
            out = 0  # R1
        results.append({"out": out})
        # R3/R4/R5/R6/R7: posedge update
        if vec["reset"] == 1:
            state = A  # R3
        else:
            if state == A:
                state = B if vec["in"] == 1 else A  # R4
            elif state == B:
                state = B if vec["in"] == 1 else C  # R5
            elif state == C:
                state = D if vec["in"] == 1 else A  # R6
            elif state == D:
                state = B if vec["in"] == 1 else C  # R7
    return results

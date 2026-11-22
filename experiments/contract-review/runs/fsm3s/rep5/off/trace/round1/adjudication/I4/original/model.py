def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; choose A)
    out = 0
    results = []

    for vec in vectors:
        # R1/R2: combinational output based on current state (visible same cycle)
        if state == A or state == B or state == C:
            out = 0  # R1
        elif state == D:
            out = 1  # R2

        # Record output for this row (sampled after posedge settles)
        results.append({"out": out & 1})

        # R3: synchronous active high reset forces state A at posedge
        if vec.get("reset", 0) == 1:
            state = A  # R3
        else:
            inp = vec.get("in", 0)
            # R4-R7: state transitions at posedge
            if state == A:
                state = A if inp == 0 else B  # R4
            elif state == B:
                state = C if inp == 0 else B  # R5
            elif state == C:
                state = A if inp == 0 else D  # R6
            elif state == D:
                state = C if inp == 0 else B  # R7

    return results

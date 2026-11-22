def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    # R1/R2: output is combinational from state (D -> 1, else 0)
    def out_of(state):
        return 1 if state == D else 0

    # global: initial state is D before any reset
    state = D
    results = []
    for vec in vectors:
        # Sample inputs at posedge (values driven before edge)
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)
        # R1/R2: combinational output visible same cycle based on current state
        results.append({'out': out_of(state)})
        # R3: synchronous active high reset -> state A (priority 0)
        if rst == 1:
            state = A
        else:
            # R4-R7: state transitions on posedge
            if state == A:
                state = B if inp == 1 else A  # R4
            elif state == B:
                state = B if inp == 1 else C  # R5
            elif state == C:
                state = D if inp == 1 else A  # R6
            elif state == D:
                state = B if inp == 1 else C  # R7
    return results

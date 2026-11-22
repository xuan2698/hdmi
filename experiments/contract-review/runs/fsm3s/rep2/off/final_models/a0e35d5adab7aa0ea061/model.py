def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    # R3: synchronous active high reset resets FSM to state A
    state = A  # initial state assumed A (uncertain global rule)
    out = 0
    results = []
    for vec in vectors:
        # Sample inputs at posedge (values driven before sampled edge)
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)
        # R1: combinational output for states A, B, C -> 0
        # R2: combinational output for state D -> 1
        if state == D:
            out = 1
        else:
            out = 0
        results.append({'out': out})
        # R3: synchronous reset has priority 0
        if rst == 1:
            state = A
        else:
            # R4: state A transitions
            if state == A:
                state = B if inp == 1 else A
            # R5: state B transitions
            elif state == B:
                state = B if inp == 1 else C
            # R6: state C transitions
            elif state == C:
                state = D if inp == 1 else A
            # R7: state D transitions
            elif state == D:
                state = B if inp == 1 else C
    return results

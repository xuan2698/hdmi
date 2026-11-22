def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    A, B, C, D = 0, 1, 2, 3
    # R3: synchronous active high reset resets FSM to state A
    state = A
    out = 0
    results = []
    for vec in vectors:
        # Sample inputs at posedge (values driven before sampled edge)
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)
        # R1/R2: combinational output based on current state (same_cycle)
        if state == D:
            out = 1  # R2
        else:
            out = 0  # R1
        results.append({'out': out})
        # R3: synchronous reset has priority 0
        if rst == 1:
            state = A
        else:
            # R4-R7: state transitions (priority 2)
            if state == A:
                state = B if inp == 1 else A  # R4
            elif state == B:
                state = B if inp == 1 else C  # R5
            elif state == C:
                state = D if inp == 1 else A  # R6
            elif state == D:
                state = B if inp == 1 else C  # R7
        # mid changes occur AFTER sampling, before other edge, carried to next row
        # (handled implicitly since next iteration reads vec's inputs)
    return results

def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up unspecified; start at reset state A
    out = 0
    results = []

    for vec in vectors:
        # Apply mid changes carried from previous row (already applied to vec)
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)

        # R1/R2: output is registered on posedge (next-cycle) per candidate interpretation
        # So we compute output from current state, but it becomes visible next cycle.
        # We'll emit the output that was registered at the previous posedge.
        results.append({'out': out})

        # Compute next state and next registered output at posedge
        if rst == 1:
            # R3: synchronous active high reset -> state A, out 0
            state = A
            out = 0
        else:
            # R4-R7: state transitions
            if state == A:
                state = B if inp == 1 else A
            elif state == B:
                state = B if inp == 1 else C
            elif state == C:
                state = D if inp == 1 else A
            elif state == D:
                state = B if inp == 1 else C
            # R1/R2: registered output based on new state
            out = 1 if state == D else 0

    return results

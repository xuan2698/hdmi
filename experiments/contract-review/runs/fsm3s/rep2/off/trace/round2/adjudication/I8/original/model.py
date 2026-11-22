def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3

    # R3: synchronous active high reset resets FSM to state A.
    # Global uncertainty: initial state before first reset assumed A (per examples).
    state = A

    results = []
    for vec in vectors:
        # Sample inputs at posedge (values driven before sampled edge).
        in_val = vec.get('in', 0) & 1
        reset_val = vec.get('reset', 0) & 1

        # R1 / R2: combinational output based on current state (same_cycle).
        if state == D:
            out_val = 1  # R2
        else:
            out_val = 0  # R1 (A, B, C)

        results.append({'out': out_val & 1})

        # R3: synchronous reset takes priority (priority 0).
        if reset_val == 1:
            state = A
        else:
            # R4-R7: explicit transitions (priority 2).
            if state == A:
                # R4: A -> A if in==0, B if in==1
                state = B if in_val == 1 else A
            elif state == B:
                # R5: B -> C if in==0, B if in==1
                state = B if in_val == 1 else C
            elif state == C:
                # R6: C -> A if in==0, D if in==1
                state = D if in_val == 1 else A
            elif state == D:
                # R7: D -> C if in==0, B if in==1
                state = B if in_val == 1 else C

        # Mid input changes occur AFTER sampling, before other edge,
        # carried to start of next row. Since we re-read vec inputs each
        # iteration, mid changes are naturally handled by the next row's
        # input values.

    return results

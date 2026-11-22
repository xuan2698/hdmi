def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # Output is combinational: out = 1 iff state == D
    # Synchronous active-high reset forces state A on posedge.
    # Initial state is A (per candidate interpretation for global).
    state = 0  # A

    results = []
    for vec in vectors:
        # Sample inputs at the posedge (values driven before edge)
        in_val = vec.get('in', 0) & 1
        reset_val = vec.get('reset', 0) & 1

        # R1/R2/R3/R4: combinational output based on current state (same_cycle)
        # out = 1 iff state == D
        out_val = 1 if state == 3 else 0  # R4 (state D -> 1); R1,R2,R3 -> 0

        results.append({'out': out_val})

        # R5: synchronous active high reset -> next state A (priority 0)
        if reset_val == 1:
            state = 0  # A
        else:
            # R6: A && in==0 -> A; A && in==1 -> B
            # R7: B && in==0 -> C; B && in==1 -> B
            # R8: C && in==0 -> A; C && in==1 -> D
            # R9: D && in==0 -> C; D && in==1 -> B
            if state == 0:      # A
                state = 0 if in_val == 0 else 1  # R6
            elif state == 1:    # B
                state = 2 if in_val == 0 else 1  # R7
            elif state == 2:    # C
                state = 0 if in_val == 0 else 3  # R8
            else:               # D
                state = 2 if in_val == 0 else 1  # R9

    return results

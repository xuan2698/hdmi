def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # Output: A->0, B->0, C->0, D->1
    # Synchronous active-high reset forces state A on posedge.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    state = 0  # power-up unspecified; start at A (R6 interpretation: initial state = source state)
    out = 0

    results = []

    for vec in vectors:
        # Apply mid changes from previous row are already reflected in vec.
        # Sample inputs at this row (driven before the sampled edge).
        in_val = vec.get('in', 0)
        reset_val = vec.get('reset', 0)

        # R1-R4: combinational output based on current state (visible same_cycle)
        # R1: state == A -> out 0
        # R2: state == B -> out 0
        # R3: state == C -> out 0
        # R4: state == D -> out 1
        if state == 0:      # R1
            out = 0
        elif state == 1:    # R2
            out = 0
        elif state == 2:    # R3
            out = 0
        elif state == 3:    # R4
            out = 1

        results.append({'out': out})

        # Posedge update (next state computed from current state and inputs)
        # R5: synchronous active high reset forces state A
        if reset_val == 1:
            state = 0  # R5
        else:
            # R6-R9: state transitions
            if state == 0:      # R6: A -> A if in==0, B if in==1
                state = 0 if in_val == 0 else 1
            elif state == 1:    # R7: B -> C if in==0, B if in==1
                state = 2 if in_val == 0 else 1
            elif state == 2:    # R8: C -> A if in==0, D if in==1
                state = 0 if in_val == 0 else 3
            elif state == 3:    # R9: D -> C if in==0, B if in==1
                state = 2 if in_val == 0 else 1

    return results

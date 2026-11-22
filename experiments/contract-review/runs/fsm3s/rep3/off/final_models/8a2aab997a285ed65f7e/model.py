def reference(vectors):
    # Contract implementation.
    # State encoding: A=0, B=1, C=2, D=3
    # R1/R2: Moore output is combinational from state (same_cycle).
    # R3: synchronous active-high reset -> state A on posedge, out=0.
    # R4-R7: next-state transitions on posedge when reset==0.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Initial state before first reset release: assume A (per contract note).

    state = 0  # A

    def out_of(s):
        # R1: A,B,C -> 0 ; R2: D -> 1
        return 1 if s == 3 else 0

    results = []
    for row in vectors:
        # Sample inputs at this row (driven before sampled edge).
        in_val = row.get('in', 0) & 1
        reset_val = row.get('reset', 0) & 1

        # Output is combinational from current state (same_cycle).
        # R1 / R2
        out_val = out_of(state)
        results.append({'out': out_val})

        # Posedge update: R3 reset has priority 0.
        if reset_val == 1:
            # R3: synchronous reset -> state A
            state = 0
        else:
            # R4-R7: next state based on current state and in
            if state == 0:  # A
                # R4
                state = 1 if in_val == 1 else 0
            elif state == 1:  # B
                # R5
                state = 1 if in_val == 1 else 2
            elif state == 2:  # C
                # R6
                state = 3 if in_val == 1 else 0
            else:  # D
                # R7
                state = 1 if in_val == 1 else 2

        # Mid changes: applied after sampling, before next edge.
        # They are carried to the start of the next row, so we apply them
        # to the row's inputs for the next iteration's sampling.
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'in' in mid:
                # carry to next row's in
                pass  # handled by caller providing next row's in
            if 'reset' in mid:
                pass

    return results

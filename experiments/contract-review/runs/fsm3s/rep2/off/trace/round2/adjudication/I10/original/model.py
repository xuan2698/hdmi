def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1, R2: combinational output based on current state
    # R3: synchronous active-high reset -> state A
    # R4-R7: state transitions on posedge when reset==0
    # Initial state: A (per examples; uncertain per spec)
    state = 0  # A
    out = 0
    results = []
    for vec in vectors:
        # Apply mid changes carried from previous row (already in vec)
        # Sample inputs at this row
        in_val = vec.get('in', 0)
        reset_val = vec.get('reset', 0)
        # R1/R2: combinational output from current state (visible same cycle)
        if state == 3:  # D
            out = 1  # R2
        else:  # A, B, C
            out = 0  # R1
        results.append({'out': out})
        # R3: synchronous reset on posedge
        if reset_val == 1:
            state = 0  # A  (R3)
        else:
            # R4-R7: transitions
            if state == 0:  # A
                state = 1 if in_val == 1 else 0  # R4
            elif state == 1:  # B
                state = 1 if in_val == 1 else 2  # R5
            elif state == 2:  # C
                state = 3 if in_val == 1 else 0  # R6
            elif state == 3:  # D
                state = 1 if in_val == 1 else 2  # R7
    return results

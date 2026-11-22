def reference(vectors):
    # Moore FSM: states A=0, B=1, C=2, D=3
    # Transitions (in=0, in=1): A->(A,B), B->(C,B), C->(A,D), D->(C,B)
    # Output: 1 only in state D
    # Synchronous active-high reset -> state A
    # Each row: drive inputs before posedge, sample after posedge settles.
    # Mid changes occur after sampling, before negedge, carried to next row start.
    next_state = [
        [0, 1],  # A
        [2, 1],  # B
        [0, 3],  # C
        [2, 1],  # D
    ]
    out_val = [0, 0, 0, 1]

    state = 0  # power-up unspecified; start at A
    pending_in = None
    pending_reset = None
    results = []

    for row in vectors:
        # Apply carried mid changes from previous row (before sampled edge)
        if pending_in is not None:
            row = dict(row)
            row['in'] = pending_in
        if pending_reset is not None:
            row = dict(row)
            row['reset'] = pending_reset
        pending_in = None
        pending_reset = None

        # Values driven before sampled edge
        in_val = row.get('in', 0)
        reset_val = row.get('reset', 0)

        # Sample at posedge: synchronous reset takes priority
        if reset_val:
            state = 0
        else:
            state = next_state[state][in_val & 1]

        # Output after edge settles (Moore: depends only on state)
        results.append({'out': out_val[state]})

        # Mid changes AFTER sampling, before other edge, carried to next row
        if 'mid_in' in row:
            pending_in = row['mid_in']
        if 'mid_reset' in row:
            pending_reset = row['mid_reset']

    return results

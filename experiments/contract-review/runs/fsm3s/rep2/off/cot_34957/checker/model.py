def reference(vectors):
    # Moore FSM: states A=0, B=1, C=2, D=3
    # next[state][in] -> next state
    # out[state] -> output
    next_state = [
        [0, 1],  # A: in=0->A, in=1->B
        [2, 1],  # B: in=0->C, in=1->B
        [0, 3],  # C: in=0->A, in=1->D
        [2, 1],  # D: in=0->C, in=1->B
    ]
    out = [0, 0, 0, 1]

    state = 0  # unspecified power-up; don't-care until first reset edge
    results = []

    for row in vectors:
        # Determine the input value sampled at this edge.
        # If 'in' is provided in the row, it drives the edge; otherwise
        # carry over the mid-row value from the previous row.
        if 'in' in row:
            in_val = row['in'] & 1
        else:
            in_val = carry_in if 'carry_in' in dir() else 0

        reset_val = row.get('reset', 0) & 1

        # Apply reset first (dominates next-state and observed output),
        # then transition, then read Moore output.
        if reset_val:
            state = 0
        else:
            state = next_state[state][in_val]

        results.append({'out': out[state] & 1})

        # Mid-row input change: occurs AFTER sampling, carried to next row.
        if 'mid_in' in row:
            carry_in = row['mid_in'] & 1
        else:
            carry_in = in_val

    return results

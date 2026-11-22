def reference(vectors):
    # Moore FSM: output depends on current (pre-edge) state.
    # States: A=0, B=1, C=2, D=3
    # Next state table: next[state][in]
    next_state = [
        [0, 1],  # A: in=0 -> A, in=1 -> B
        [2, 1],  # B: in=0 -> C, in=1 -> B
        [0, 3],  # C: in=0 -> A, in=1 -> D
        [2, 1],  # D: in=0 -> C, in=1 -> B
    ]
    # Output per state (Moore)
    output = [0, 0, 0, 1]

    state = 0  # power-up unspecified; reset will fix it
    results = []

    for row in vectors:
        # Sample pre-edge state and input
        pre_state = state
        in_val = row.get('in', 0)
        reset_val = row.get('reset', 0)

        # Output is from pre-edge state
        out_val = output[pre_state]

        results.append({'out': out_val})

        # Apply transition at posedge with synchronous active-high reset
        if reset_val:
            state = 0  # A
        else:
            state = next_state[pre_state][in_val]

        # Mid-row input changes occur AFTER sampling, before next edge,
        # and are carried to the start of the next row. Since we read
        # 'in' fresh each row, this is naturally handled.

    return results

def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # Moore outputs: A=0, B=0, C=0, D=1
    # Synchronous active-high reset forces state A at posedge.
    # Output is determined by the state entered at the sampled posedge.
    out_bits = 1
    state = 0  # power-up unspecified; will be overwritten by first reset/edge
    results = []
    for row in vectors:
        # Apply inputs before the sampled edge
        inp = row.get('in', 0) & 1
        rst = row.get('reset', 0) & 1
        # Compute next state at posedge
        if rst:
            nxt = 0  # A
        else:
            if state == 0:      # A
                nxt = 0 if inp == 0 else 1
            elif state == 1:    # B
                nxt = 2 if inp == 0 else 1
            elif state == 2:    # C
                nxt = 0 if inp == 0 else 3
            else:               # D
                nxt = 2 if inp == 0 else 1
        state = nxt
        # Moore output of the newly entered state
        out = 1 if state == 3 else 0
        results.append({'out': out & ((1 << out_bits) - 1)})
    return results

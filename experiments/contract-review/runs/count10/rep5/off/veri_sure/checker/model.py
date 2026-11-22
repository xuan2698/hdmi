def reference(vectors):
    # Decade counter: counts 0..9, synchronous active-high reset to 0.
    # Output q has latency 1 cycle (reflects state after the sampled posedge).
    # Each row: inputs driven before the sampled posedge; mid changes occur
    # AFTER sampling (before the next edge) and carry to the start of next row.
    out = []
    state = 0  # power-up unspecified; use 0 as concrete value
    for row in vectors:
        # Apply any mid changes from the previous row are already carried in
        # via 'row' inputs (they represent values at the sampled edge).
        reset = row.get('reset', 0) & 1
        # Compute next state based on current state and reset at this edge
        if reset:
            nxt = 0
        elif state == 9:
            nxt = 0
        else:
            nxt = state + 1
        # Output reflects state after the edge settles (latency 1)
        state = nxt
        out.append({'q': state & 0xF})
    return out

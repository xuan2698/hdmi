def reference(vectors):
    # Decade counter, active-high synchronous reset, counts 0..9.
    # State persists across rows. For each row, the sampled inputs drive the
    # next-state computation at the posedge; mid changes apply to the next row.
    q = 0
    out = []
    for row in vectors:
        # Sample inputs for this row (values driven before the sampled edge).
        reset = row.get('reset', 0) & 1
        # Compute next state from current q and sampled reset.
        if reset:
            nq = 0
        else:
            nq = q + 1
            if nq > 9:
                nq = 0
        # Output is the settled value after the edge.
        out.append({'q': nq & 0xF})
        # Mid changes occur after sampling; they affect the next row's inputs,
        # which are already provided by the next row's driven values.
        q = nq
    return out

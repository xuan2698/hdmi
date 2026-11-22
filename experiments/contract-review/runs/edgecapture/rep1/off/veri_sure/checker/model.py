def reference(vectors):
    # Contract:
    # - clk posedge sampling; reset is active-high synchronous, priority over detection.
    # - out[i] set to 1 when in[i] goes 1 -> 0 between consecutive sampled edges.
    # - out is sticky until reset.
    # - Output reflects state after the sampled edge (1-cycle latency).
    # - Mid changes occur AFTER sampling, before the other edge, carried to next row.
    out = 0
    prev_in = 0
    prev_valid = False
    results = []
    for row in vectors:
        # Apply mid changes from previous row (already applied before this row's sampling)
        # Determine sampled values at this posedge
        reset_val = row.get('reset', 0)
        in_val = row.get('in', 0)
        # Sample: compute new out based on prev_in and current in
        if reset_val:
            out = 0
        else:
            if prev_valid:
                # detect 1->0 transitions
                trans = prev_in & (~in_val) & 0xFFFFFFFF
                out = (out | trans) & 0xFFFFFFFF
            # if not prev_valid, no transition detection (first edge)
        prev_in = in_val & 0xFFFFFFFF
        prev_valid = True
        results.append({'out': out & 0xFFFFFFFF})
    return results

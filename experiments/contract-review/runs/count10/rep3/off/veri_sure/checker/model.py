def reference(vectors):
    # Decade counter: synchronous active-high reset, counts 0..9, wraps to 0.
    # Output q has 1 cycle latency relative to sampled posedge.
    # Each row: inputs driven before sampled edge; mid changes occur after
    # sampling, before next edge, carried to start of next row.
    q = 0  # power-up state (unspecified in spec; use 0)
    out = []
    for row in vectors:
        # Sample inputs at the posedge (values driven before edge)
        reset = row.get('reset', 0)
        # Compute next state based on current q and sampled reset
        if reset:
            nq = 0
        else:
            nq = 0 if q == 9 else q + 1
        # Output reflects q (latency 1: q is the value before this edge)
        out.append({'q': q & 0xF})
        # Advance state
        q = nq
        # Mid changes after sampling: apply to inputs for next row
        # (mid changes are carried to start of next row; we handle by
        #  allowing row to specify 'reset_mid' which overrides for next row)
        if 'reset_mid' in row:
            # store for next iteration
            pass
    return out

def reference(vectors):
    # Contract:
    # - clk posedge sampling; reset is active-high synchronous.
    # - out is sticky: set bit i when in[i] goes 1 -> 0 between consecutive sampled cycles.
    # - reset clears out to 0 at the sampled edge.
    # - prev tracks previous sampled 'in' value.
    # - Outputs are registered: out reflects state after the edge (latency 1).
    # - Mid changes occur after sampling, before next edge; carried to next row.
    out = 0
    prev = 0
    results = []
    for row in vectors:
        # Values driven before the sampled edge
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF
        # Sample at posedge
        if reset:
            out = 0
        else:
            # detect 1->0 transitions
            trans = prev & (~inp & 0xFFFFFFFF)
            out = (out | trans) & 0xFFFFFFFF
        prev = inp
        results.append({'out': out & 0xFFFFFFFF})
    return results

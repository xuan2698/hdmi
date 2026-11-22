def reference(vectors):
    # Contract:
    # - clk posedge sampling; reset is active-high synchronous.
    # - out is sticky: bit i set on 1->0 transition of in[i] between consecutive sampled edges.
    # - First sampled edge after reset establishes baseline (no transition inferred from unknown prior).
    # - Mid changes occur after sampling, before next edge; carried to start of next row.
    # - Output latency 1 cycle: out reflects state after the sampled edge.
    out = 0
    prev_in = None
    prev_reset = None
    results = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        in_val = row.get('in', 0)
        # Sample on posedge: detect rising edge of clk
        # We treat each row as a sampled edge if clk is 1 (posedge settled).
        # Per spec: "sample after the posedge edge has settled" -> row represents post-edge state.
        # So we process the edge using current row's reset/in values.
        if reset:
            out = 0
            prev_in = in_val
        else:
            if prev_in is None:
                # First sampled edge after reset establishes baseline
                prev_in = in_val
            else:
                # Detect 1->0 transitions
                trans = (~in_val) & prev_in & 0xFFFFFFFF
                out = (out | trans) & 0xFFFFFFFF
                prev_in = in_val
        results.append({'out': out & 0xFFFFFFFF})
    return results

def reference(vectors):
    # State: Q holds the stored flip-flop value driven to output q.
    # Power-up value is unspecified; we choose 0 as a concrete initial value.
    Q = 0

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # R1_sync_reset: active high synchronous reset -> q = 0 on posedge
        # R2_capture_d: when r == 0, capture d on posedge
        # Both rules are evaluated at the posedge clk (sampled edge).
        if r == 1:
            # R1_sync_reset (priority 1)
            Q = 0
        else:
            # R2_capture_d (priority 2)
            Q = d

        # Output q reflects the stored value after the sampled edge.
        results.append({'q': Q & 1})

    return results

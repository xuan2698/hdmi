def reference(vectors):
    # State: Q = stored flip-flop value, initializes to 1 at time zero (candidate interpretation)
    Q = 1  # R_global: Q initializes to 1 at time zero before any clock edge

    results = []
    for row in vectors:
        d = row['d']
        r = row['r']

        # Sample at posedge clk (values driven before the sampled edge)
        # R1_sync_reset: r == 1 -> q = 0, priority 1
        if r == 1:
            Q = 0
        else:
            # R2_capture_d: r == 0 -> q = d, priority 2
            Q = d & 1

        # Output q reflects stored value (same_cycle visibility)
        results.append({'q': Q & 1})

        # Mid input changes occur AFTER sampling, before the other edge,
        # carried to the start of the next row. No state change here.

    return results

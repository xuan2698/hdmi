def reference(vectors):
    # Initial state q is unspecified at power-up; choosing concrete 0.
    # It will be updated at the first sampled posedge.
    q = 0
    results = []

    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1

        # Rule sync_active_high_reset: At the sampled posedge clk, if r == 1,
        # q is updated to 0 regardless of d. Reset has priority 2.
        if r == 1:
            q = 0
        else:
            # Rule d_capture_when_not_reset: At the sampled posedge clk, if r == 0,
            # q is updated to the sampled value of d. Priority 1.
            q = d

        # Output q is the state after the sampled posedge (visible same_cycle).
        # Mid-cycle changes occur after sampling and only affect the next row's
        # sampled inputs, which are already represented in the next row's values.
        results.append({'q': q})

    return results

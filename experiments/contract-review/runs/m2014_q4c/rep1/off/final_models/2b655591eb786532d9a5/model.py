def reference(vectors):
    # State: Q = stored flip-flop value (power-up unspecified; use 0)
    Q = 0

    results = []

    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1

        # R1_sync_reset: on posedge, if r == 1, q <= 0 (priority 1)
        # R2_capture_d: on posedge, if r == 0, q <= d (priority 2)
        if r == 1:
            Q = 0  # R1_sync_reset
        else:
            Q = d  # R2_capture_d

        results.append({'q': Q & 1})

    return results

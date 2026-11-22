def reference(vectors):
    # Contract implementation.
    # State: Q = stored flip-flop value (driven to q).
    # Update time: posedge clk. Synchronous active-high reset r.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    Q = 0  # power-up unspecified; choose 0 as concrete value

    out = []
    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1

        # R1_sync_reset: r == 1 -> q = 0 on posedge (priority 1)
        # R2_capture_d:  r == 0 -> q = d on posedge (priority 2)
        if r == 1:
            Q = 0
        else:
            Q = d

        out.append({'q': Q & 1})

    return out

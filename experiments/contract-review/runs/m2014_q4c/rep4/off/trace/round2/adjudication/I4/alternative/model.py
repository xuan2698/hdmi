def reference(vectors):
    # State: Q = stored flip-flop value (initialized to 0 per candidate interpretation)
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # posedge clk sampling:
        # R1_sync_reset: r == 1 at posedge -> q <= 0 (priority 1)
        # R2_capture_d: r == 0 at posedge -> q <= d (priority 2)
        if r == 1:
            Q = 0  # R1_sync_reset
        else:
            Q = d  # R2_capture_d
        out.append({'q': Q & 1})
    return out

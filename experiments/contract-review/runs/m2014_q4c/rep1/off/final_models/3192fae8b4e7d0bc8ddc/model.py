def reference(vectors):
    # State: Q = stored flip-flop value (driven to q)
    Q = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1
        # R1_sync_reset: on posedge, if r==1, q <= 0 (priority 1)
        # R2_capture_d: on posedge, if r==0, q <= d (priority 2)
        if r == 1:
            Q = 0  # R1_sync_reset
        else:
            Q = d  # R2_capture_d
        out.append({'q': Q & 1})
        # mid changes occur AFTER sampling; carried to next row (no action needed here)
    return out

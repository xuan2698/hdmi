def reference(vectors):
    # State: Q = stored flip-flop value (power-up unspecified -> start at 0)
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # R1_sync_reset: active high synchronous reset, priority 1
        # R2_capture_d: capture d on posedge when r == 0, priority 2
        if r == 1:
            Q = 0  # R1_sync_reset
        else:
            Q = d  # R2_capture_d
        out.append({'q': Q & 1})
    return out

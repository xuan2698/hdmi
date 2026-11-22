def reference(vectors):
    # State: Q = stored flip-flop value (power-up unspecified -> start at 0)
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # R1_sync_reset: active high synchronous reset (reset output to 0)
        # Candidate interpretation: data capture takes priority over reset when r==1 and d sampled
        # R2_capture_d: capture d on posedge when r==0
        if r == 1:
            # R1_sync_reset with candidate interpretation: q follows d instead of resetting
            Q = d
        else:
            # R2_capture_d
            Q = d
        out.append({'q': Q & 1})
    return out

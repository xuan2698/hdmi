def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop storage (R1_sync_reset, R2_d_capture)
    q_reg = 0  # power-up unspecified; use concrete 0
    out = []
    for row in vectors:
        # Inputs driven before the sampled posedge
        d = row['d'] & 0xFF
        reset = row['reset'] & 0x1
        # R1_sync_reset: active high synchronous reset -> q=0 on posedge (priority 1)
        # R2_d_capture: reset==0 -> q=d on posedge (priority 2)
        if reset == 1:
            q_reg = 0
        else:
            q_reg = d
        # Sample after posedge settled
        out.append({'q': q_reg & 0xFF})
        # Mid changes occur AFTER sampling; carried to next row (no state change here)
    return out

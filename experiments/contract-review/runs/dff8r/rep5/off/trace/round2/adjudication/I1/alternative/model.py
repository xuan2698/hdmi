def reference(vectors):
    # Contract implementation.
    # State: q_reg holds the 8-bit flip-flop storage (initial 0 before any posedge).
    # R1_sync_reset: on posedge, if reset==1, q <= 0 (priority 1).
    # R2_d_capture: on posedge, if reset==0, q <= d (priority 2).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Initial q is unspecified/X until first posedge; only reset forces 0.
    # We model initial as 0 (concrete unsigned integer required per row).
    q_reg = 0  # initial value before any posedge clk
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # Sample at posedge: compute next state from current inputs.
        # R1_sync_reset (priority 1)
        if reset == 1:
            q_reg = 0
        else:
            # R2_d_capture (priority 2)
            q_reg = d
        # Output visible same cycle after posedge.
        out.append({'q': q_reg & 0xFF})
        # Mid changes (if any) occur AFTER sampling; they affect next row's inputs,
        # which are already provided by the next row's d/reset values.
    return out

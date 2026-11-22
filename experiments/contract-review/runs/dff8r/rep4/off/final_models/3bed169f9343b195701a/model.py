def reference(vectors):
    # Contract implementation.
    # State: q_reg (8-bit), updated at posedge clk.
    # R1_sync_reset: reset==1 at posedge -> q <= 0 (priority 1)
    # R2_dff_capture: reset==0 at posedge -> q <= d (priority 2)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    q_reg = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)
        # Sample at posedge: compute next state based on current inputs
        # R1_sync_reset (priority 1)
        if reset == 1:
            q_reg = 0
        else:
            # R2_dff_capture (priority 2)
            q_reg = d & 0xFF
        out.append({'q': q_reg & 0xFF})
        # Mid changes: applied after sampling, carried to next row.
        # Since we read inputs fresh each row, mid changes are naturally
        # reflected in the next row's inputs.
    return out

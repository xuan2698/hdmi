def reference(vectors):
    # Contract implementation.
    # State: q_state, 8-bit register, updates at negedge of clk.
    # R1_sync_reset: reset==1 at negedge -> q <= 52 (0x34), priority 1.
    # R2_dff_capture: reset==0 at negedge -> q <= d, priority 2.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    q_state = 52  # power-up value per reset spec (0x34)
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # Sample at negedge: apply rules in priority order.
        if reset == 1:
            # R1_sync_reset
            q_state = 52
        else:
            # R2_dff_capture
            q_state = d
        out.append({'q': q_state & 0xFF})
    return out

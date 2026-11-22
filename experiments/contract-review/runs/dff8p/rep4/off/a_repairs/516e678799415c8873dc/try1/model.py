def reference(vectors):
    # State: q_reg holds the 8 D flip-flop outputs.
    # Reset value is 0x34 (52). Updated on negedge clk.
    # R1_sync_reset / R3_reset_value: reset==1 at negedge -> q becomes 0x34 (same cycle visible).
    # R2_dff_capture: reset==0 at negedge -> q captures d.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    q_reg = 0x34  # power-up unspecified; use reset value as concrete default
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # negedge sampling: apply reset or capture
        if reset == 1:
            # R1_sync_reset, R3_reset_value
            q_reg = 0x34
        else:
            # R2_dff_capture
            q_reg = d
        out.append({'q': q_reg & 0xFF})
        # mid changes after sampling are carried to next row (no state change here)
    return out

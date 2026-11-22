def reference(vectors):
    # State: q_reg holds the 8 D flip-flop outputs.
    # R3_reset_value: reset value is 0x34 (52), not zero.
    q_reg = 0x34  # power-up unspecified; use reset value as concrete default

    out = []
    for row in vectors:
        d = row.get("d", 0) & 0xFF
        reset = row.get("reset", 0) & 0x1

        # R1_sync_reset: active-high synchronous reset on negedge clk.
        # R3_reset_value: reset loads 0x34.
        # R2_dff_capture: otherwise capture d on negedge clk.
        if reset == 1:
            q_reg = 0x34  # R1_sync_reset, R3_reset_value
        else:
            q_reg = d  # R2_dff_capture

        out.append({"q": q_reg & 0xFF})

    return out

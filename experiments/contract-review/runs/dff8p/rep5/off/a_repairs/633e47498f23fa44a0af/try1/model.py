def reference(vectors):
    # State: q_state holds the 8-bit register value.
    # R1_sync_reset: on negedge, if reset==1, q_state <= 0x34 (52).
    # R2_dff_capture: on negedge, if reset==0, q_state <= d.
    # Initial value: power-up unspecified; use 0x34 to match reset value
    # so that the first sampled negedge with reset==1 yields 52.
    q_state = 0x34  # R1_sync_reset (initial register value)
    out = []
    for row in vectors:
        d = row.get("d", 0) & 0xFF
        reset = row.get("reset", 0) & 0x1
        # negedge sampling: apply synchronous reset or capture d
        if reset == 1:
            q_state = 0x34  # R1_sync_reset
        else:
            q_state = d  # R2_dff_capture
        out.append({"q": q_state & 0xFF})
    return out

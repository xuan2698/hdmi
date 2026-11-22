def reference(vectors):
    # Contract implementation.
    # State: Q = 8-bit flip-flop output register, reset value 0x34 (52).
    # Update time: negedge of clk. Sample after negedge has settled.
    # Each row's values are driven before the sampled edge.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    Q = 0x34  # power-up / initial state value (R3_reset_value)
    out = []

    for row in vectors:
        d = row.get("d", 0) & 0xFF
        reset = row.get("reset", 0) & 0x1

        # R1_sync_reset: reset == 1 at negedge -> Q = 0x34, priority 1
        # R3_reset_value: reset value is 0x34 (52)
        # R2_dff_capture: reset == 0 at negedge -> Q = d, priority 2
        if reset == 1:
            Q = 0x34
        else:
            Q = d

        # visible same_cycle: output reflects the negedge update
        out.append({"q": Q & 0xFF})

    return out

def reference(vectors):
    # Contract implementation.
    # State: Q = 8-bit flip-flop output register, reset value 0x34 (52).
    # Update time: negedge of clk. Sample after negedge has settled.
    # Each row's values are driven before the sampled edge.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    Q = 0x34  # power-up / initial state (R3_reset_value base)

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # negedge sampling: apply synchronous reset or capture d
        if reset == 1:
            # R1_sync_reset: active high synchronous reset, priority 1
            # R3_reset_value: reset value is 0x34 (52), not zero
            Q = 0x34
        else:
            # R2_dff_capture: capture d on negedge when reset == 0
            Q = d

        # Output visible same cycle
        results.append({'q': Q & 0xFF})

    return results

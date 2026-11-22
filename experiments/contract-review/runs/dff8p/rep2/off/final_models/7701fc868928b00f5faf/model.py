def reference(vectors):
    # Contract implementation.
    # State Q: 8-bit flip-flop output register, reset value 0x34.
    # Update on negedge of clk. Reset is active-high synchronous.
    # R1_sync_reset: reset==1 overrides d on same negedge (priority 1).
    # R2_dff_capture: reset==0 -> q captures d on negedge (priority 2).
    # R3_reset_value: reset value is 0x34 (52), not 0.
    # Mid input changes occur AFTER sampling, before other edge,
    # carried to start of next row.

    Q = 0x34  # power-up / initial state value (R3_reset_value)
    out = []

    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # Sample at negedge: apply synchronous reset or capture d.
        if reset == 1:
            # R1_sync_reset (priority 1): reset overrides d, same-cycle visible
            Q = 0x34  # R3_reset_value
        else:
            # R2_dff_capture (priority 2): capture d on negedge
            Q = d & 0xFF

        # Output visible same cycle
        out.append({'q': Q & 0xFF})

        # Mid changes: after sampling, before other edge, carried to next row.
        # (No separate mid handling needed here since next row's d/reset
        #  already reflect the carried values.)

    return out

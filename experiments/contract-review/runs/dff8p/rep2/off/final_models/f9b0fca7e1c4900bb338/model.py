def reference(vectors):
    # Contract implementation.
    # State: Q is the 8-bit flip-flop output register, reset value 0x34 (52).
    # Clock: negedge of clk. Each row's inputs are driven before the sampled negedge.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Outputs are visible same cycle as the sampled negedge.

    Q = 0x34  # R3_reset_value: power-up / reset value 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # Sample at negedge: apply synchronous reset or capture d.
        if reset == 1:
            # R1_sync_reset: active high synchronous reset, priority 1, same cycle
            Q = 0x34  # R3_reset_value: reset to 0x34
        else:
            # R2_dff_capture: capture d on negedge, same cycle
            Q = d

        results.append({'q': Q & 0xFF})

    return results

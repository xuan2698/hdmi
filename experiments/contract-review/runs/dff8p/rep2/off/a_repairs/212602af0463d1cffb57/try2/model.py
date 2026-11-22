def reference(vectors):
    # State: Q register, reset value 0x34 (52)
    Q = 0x34  # R3_reset_value: power-up/reset value 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)

        # R1_sync_reset: active high synchronous reset, priority 1, negedge, same_cycle
        # R2_dff_capture: reset==0, negedge, same_cycle
        # R3_reset_value: reset to 0x34 at negedge
        if reset == 1:
            Q = 0x34  # R1_sync_reset, R3_reset_value
        else:
            Q = d & 0xFF  # R2_dff_capture

        results.append({'q': Q & 0xFF})

    return results

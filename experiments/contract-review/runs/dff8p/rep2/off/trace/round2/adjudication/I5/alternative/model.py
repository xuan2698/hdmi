def reference(vectors):
    # State: Q register, 8-bit flip-flop output
    # Initial q is 0x00 before any reset or clock edge (candidate interpretation for global)
    Q = 0x00

    results = []
    for row in vectors:
        d = row['d'] & 0xFF
        reset = row['reset'] & 0x1

        # R1_sync_reset: reset == 1 at negedge -> q = 0x34 (priority 1)
        # R3_reset_value: reset value is 0x34 (52)
        # R2_dff_capture: reset == 0 at negedge -> q = d (priority 2)
        if reset == 1:
            Q = 0x34  # R1_sync_reset, R3_reset_value
        else:
            Q = d  # R2_dff_capture

        results.append({'q': Q & 0xFF})

    return results

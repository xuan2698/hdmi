def reference(vectors):
    # State: q_state holds the 8-bit register value of the D flip-flops.
    # Initial value is unspecified at power-up; we use 0x34 as the reset value
    # and start from it so the first sampled negedge is well-defined.
    q_state = 0x34  # R1_sync_reset: reset value is 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1_sync_reset: active high synchronous reset on negedge, priority 1
        # R2_dff_capture: otherwise capture d on negedge, priority 2
        if reset == 1:
            q_state = 0x34
        else:
            q_state = d

        # Output visible same cycle as the sampled negedge
        results.append({'q': q_state & 0xFF})

    return results

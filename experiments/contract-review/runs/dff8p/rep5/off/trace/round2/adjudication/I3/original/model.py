def reference(vectors):
    # State: q_state holds the 8-bit register value.
    # Power-up value is unspecified; use 0x34 (52) as the concrete initial value.
    q_state = 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1_sync_reset: active high synchronous reset on negedge -> q = 0x34
        # R2_dff_capture: on negedge with reset==0 -> q = d
        # Both rules are evaluated at the negedge sampling point.
        if reset == 1:
            q_state = 0x34  # R1_sync_reset
        else:
            q_state = d     # R2_dff_capture

        # Output visible same cycle after negedge settles.
        results.append({'q': q_state & 0xFF})

    return results

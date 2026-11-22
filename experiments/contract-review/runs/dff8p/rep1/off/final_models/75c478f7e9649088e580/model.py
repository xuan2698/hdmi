def reference(vectors):
    # State: q_state holds the 8-bit value stored in the D flip-flops.
    # Initial value is unspecified at power-up; we start at 0x34 (52) since
    # the reset value is 0x34 and the first sampled edge will set it anyway.
    q_state = 0x34  # R1: reset value 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1: active high synchronous reset on negedge -> q = 0x34
        # R2: reset == 0 on negedge -> q = d
        # Both rules are evaluated at the negedge sampling point.
        if reset == 1:
            q_state = 0x34  # R1
        else:
            q_state = d  # R2

        results.append({'q': q_state & 0xFF})

    return results

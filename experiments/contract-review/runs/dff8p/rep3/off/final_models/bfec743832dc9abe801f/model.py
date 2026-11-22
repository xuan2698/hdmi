def reference(vectors):
    # State: Q is the 8-bit flip-flop output register, reset value 0x34 (52).
    Q = 0x34  # power-up / initial state

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1: active high synchronous reset on negedge -> Q = 0x34, priority 1
        # R2: reset == 0 on negedge -> Q = d, priority 2
        # Both rules update on negedge and are visible same cycle.
        if reset == 1:
            Q = 0x34  # R1
        else:
            Q = d     # R2

        results.append({'q': Q & 0xFF})

    return results

def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit counter q), advances on posedge clk.
    # R1: reset == 1 on posedge -> q = 0 (sync, active high, priority 1).
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2).
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3).
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Power-up unspecified: start q = 0 (concrete value required).

    q = 0  # COUNT state, power-up concrete value
    out = []

    for row in vectors:
        # Sample inputs at posedge (values driven before sampled edge).
        reset = row.get('reset', 0) & 1

        # R1: synchronous active-high reset, priority 1
        if reset == 1:
            q = 0
        # R2: count up when q < 9, priority 2
        elif q < 9:
            q = q + 1
        # R3: wrap from 9 to 0, priority 3
        else:  # q == 9
            q = 0

        # Output visible same cycle after posedge settles.
        out.append({'q': q & 0xF})

        # Mid changes occur AFTER sampling, before other edge,
        # carried to start of next row. No mid inputs affect state here
        # beyond what is already captured in 'reset' for this row.

    return out

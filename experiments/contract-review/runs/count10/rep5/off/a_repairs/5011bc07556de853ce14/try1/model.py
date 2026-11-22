def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit counter q), advances on posedge clk.
    # R1: reset == 1 on posedge -> q = 0 (sync, active high, priority 1).
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2).
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3).
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Power-up unspecified: start at 0.

    q = 0  # COUNT state, power-up unspecified -> concrete 0
    out = []

    for row in vectors:
        # Apply any mid changes carried from previous row are already applied
        # (we apply mid after sampling below).
        reset = row.get("reset", 0)

        # Sample on posedge clk: compute next state based on current inputs.
        # R1: reset == 1 -> q = 0
        if reset == 1:
            q_next = 0
        # R2: reset == 0 && q < 9 -> q = q + 1
        elif q < 9:
            q_next = q + 1
        # R3: reset == 0 && q == 9 -> q = 0
        else:
            q_next = 0

        # Output visible same cycle (after edge settles) = new state
        q = q_next
        out.append({"q": q & 0xF})

        # Mid changes occur AFTER sampling, before other edge, carried to next row.
        # (No mid inputs in this contract beyond reset which is a row input.)

    return out

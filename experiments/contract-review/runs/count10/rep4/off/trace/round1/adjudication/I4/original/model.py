def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (0..9). Output q = COUNT.
    # R1: reset == 1 at posedge -> q = 0 (priority 1).
    # R2: reset == 0 && q < 9 at posedge -> q = q + 1.
    # R3: reset == 0 && q == 9 at posedge -> q = 0.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # COUNT state, power-up value 0
    out = []

    for row in vectors:
        # Apply any mid changes carried from previous row are already in row.
        # Sample inputs before posedge (values driven before sampled edge).
        reset = row.get("reset", 0)

        # Compute next state at posedge clk (sampled edge).
        # R1: reset == 1 -> q = 0
        if reset == 1:
            q_next = 0
        # R3: reset == 0 && q == 9 -> q = 0
        elif q == 9:
            q_next = 0
        # R2: reset == 0 && q < 9 -> q = q + 1
        else:
            q_next = q + 1

        # Output visible same cycle (after posedge settles) = new state
        q = q_next
        out.append({"q": q & 0xF})

    return out

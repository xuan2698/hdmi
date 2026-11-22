def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # State: COUNT (4-bit q), power-up value 0.
    # R1: reset == 1 at posedge -> q = 0 (same cycle, priority 1).
    # R2: reset == 0 && q < 9 at posedge -> q = q + 1 (same cycle, priority 2).
    # R3: reset == 0 && q == 9 at posedge -> q = 0 (same cycle, priority 3).
    # Mid input changes occur AFTER sampling, before the other edge, carried to next row.
    # Each row's values are driven before the sampled posedge.

    q = 0  # COUNT state, power-up value 0
    out = []

    for row in vectors:
        # Inputs are driven before the sampled posedge.
        reset = row.get("reset", 0)

        # Sample at posedge clk: compute next state per rules.
        if reset == 1:
            # R1: synchronous active-high reset -> q = 0
            q_next = 0
        elif q < 9:
            # R2: count up while q < 9
            q_next = q + 1
        else:
            # R3: q == 9 -> wrap to 0
            q_next = 0

        # Visible same cycle: output reflects the post-edge state.
        q = q_next
        out.append({"q": q & 0xF})

        # Mid changes (if any) occur after sampling; they are carried to the
        # start of the next row, so no action needed here beyond noting it.

    return out

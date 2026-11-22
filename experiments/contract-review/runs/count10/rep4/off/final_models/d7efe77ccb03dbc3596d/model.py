def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (0..9). Output q reflects the current count.
    # R1: reset == 1 at posedge -> q becomes 0 (sync reset, same-cycle visible).
    # R2: reset == 0 && q < 9 at posedge -> q becomes q + 1.
    # R3: reset == 0 && q == 9 at posedge -> q becomes 0 (period 10).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    count = 0  # named state COUNT, power-up value 0 (concrete)
    out = []

    for row in vectors:
        # Sample inputs for this row (driven before the sampled posedge).
        reset = row.get("reset", 0)

        # Evaluate next state at posedge clk.
        if reset == 1:
            # R1: synchronous active-high reset -> 0
            count = 0
        elif count < 9:
            # R2: increment while below 9
            count = count + 1
        else:
            # R3: wrap from 9 to 0
            count = 0

        # Output q visible same cycle as the sampled edge.
        out.append({"q": count & 0xF})

        # Mid changes (if any) occur after sampling; they affect the next row's
        # inputs, which are read fresh from the next row dict. No extra action needed.

    return out

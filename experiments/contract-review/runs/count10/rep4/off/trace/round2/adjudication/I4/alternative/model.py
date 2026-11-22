def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (0..9). Output q = COUNT.
    # R1: reset == 1 at posedge -> q = 0 (sync, same cycle visible).
    # R2: reset == 0 && q < 9 at posedge -> q = q + 1.
    # R3: reset == 0 && q == 9 at posedge -> q = 0 (wrap, period 10).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Power-up unspecified: we start at 0 (concrete value required).

    count = 0  # named state COUNT
    out = []

    for row in vectors:
        # Sample inputs at this row (driven before the sampled posedge).
        reset = row.get("reset", 0) & 1

        # Compute next state at posedge clk (synchronous update).
        if reset == 1:
            # R1: active high synchronous reset -> 0
            count = 0
        else:
            if count < 9:
                # R2: count up while below 9
                count = count + 1
            else:
                # R3: wrap 9 -> 0 (period 10)
                count = 0

        # Output visible same cycle after posedge settles.
        out.append({"q": count & 0xF})

        # Mid changes: applied AFTER sampling, before other edge,
        # carried to start of next row. Since we already sampled reset
        # for this row, any mid reset change affects the next row only.
        # (No explicit mid field in vectors here; handled by row order.)

    return out

def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: count (0..9). Initial value is unspecified; we choose 0.
    # R1: reset == 1 on posedge -> q = 0 (priority 1)
    # R2: reset == 0 && q == 9 on posedge -> q = 0 (wrap, priority 2)
    # R3: reset == 0 && q != 9 on posedge -> q = q + 1 (priority 3)
    # Mid changes occur after sampling, before next edge; carried to next row.

    count = 0  # initial unspecified; choose 0
    out = []

    for row in vectors:
        reset = row.get("reset", 0)
        # Sample current outputs before the posedge (values driven before edge)
        q = count & 0xF
        out.append({"q": q})

        # Apply mid changes after sampling (none defined here beyond reset carry)
        # reset value for this row is used at the posedge

        # Compute next state at posedge clk
        if reset == 1:
            # R1: synchronous active-high reset -> 0
            count = 0
        elif count == 9:
            # R2: wrap 9 -> 0
            count = 0
        else:
            # R3: increment
            count = (count + 1) % 10

    return out

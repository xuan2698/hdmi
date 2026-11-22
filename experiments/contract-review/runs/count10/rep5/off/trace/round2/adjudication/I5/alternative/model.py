def reference(vectors):
    # Contract rules:
    # R1: reset == 1 on posedge -> q = 0 (sync, priority 1)
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2)
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Power-up unspecified -> start at 0.
    # Candidate alternative (period 9) is NOT applied; contract wins.

    q = 0  # named state: COUNT
    out = []

    for row in vectors:
        # Determine reset value for this row (mid changes from prior row already applied)
        reset = row.get("reset", 0)

        # Sample at posedge clk (values driven before sampled edge)
        # R1: sync active-high reset
        if reset == 1:
            q = 0
        # R2: count up while q < 9
        elif q < 9:
            q = q + 1
        # R3: wrap from 9 to 0
        else:  # q == 9
            q = 0

        # Output visible same cycle
        out.append({"q": q & 0xF})

        # Process mid changes AFTER sampling, carried to next row
        # (mid changes are already reflected in next row's dict; nothing to do here)

    return out

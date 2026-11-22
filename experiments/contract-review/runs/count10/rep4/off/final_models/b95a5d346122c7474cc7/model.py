def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated at posedge clk.
    # Output q reflects COUNT (same_cycle visibility).
    # reset is active-high synchronous: at posedge, if reset==1 -> q=0.
    # Otherwise q advances 0..9 with period 10 (9 -> 0).
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    q = 0  # power-up unspecified; use 0 as concrete value
    out = []

    for row in vectors:
        # Mid changes from previous row are already applied to `row` here
        # (carried to start of this row). Sample at posedge.
        reset = row.get("reset", 0)

        # R1: reset == 1 -> q = 0 (priority 1)
        if reset == 1:
            q = 0
        else:
            # R2: reset == 0 && q < 9 -> q = q + 1
            # R3: reset == 0 && q == 9 -> q = 0
            if q < 9:
                q = q + 1
            else:
                q = 0

        # Output visible same cycle
        out.append({"q": q & 0xF})

    return out

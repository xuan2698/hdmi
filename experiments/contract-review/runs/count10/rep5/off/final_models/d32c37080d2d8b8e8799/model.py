def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit q). Synchronous active-high reset.
    # R1: reset == 1 at posedge -> q = 0 (priority 1).
    # R2: reset == 0 && q < 9 at posedge -> q = q + 1 (priority 2).
    # R3: reset == 0 && q == 9 at posedge -> q = 0 (priority 3).
    # Power-up: q unspecified; use 0 as concrete value.
    q = 0
    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous update based on current inputs.
        if reset == 1:
            # R1
            q = 0
        else:
            if q < 9:
                # R2
                q = q + 1
            else:
                # R3
                q = 0
        out.append({"q": q & 0xF})
        # Mid changes occur AFTER sampling; carried to next row.
        # (No mid inputs in this contract beyond reset, which is a row input.)
    return out

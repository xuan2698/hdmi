def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated at posedge clk.
    # Power-on: q = 0 (chosen candidate; unspecified in spec).
    q = 0  # R1/R2/R3 state; power-on choice

    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous reset / count transition.
        if reset == 1:
            # R1: active-high synchronous reset -> q becomes 0 (priority 1)
            q = 0
        else:
            if q < 9:
                # R2: count up while q < 9
                q = q + 1
            else:
                # R3: wrap from 9 to 0
                q = 0
        # Output visible same cycle after posedge settles.
        out.append({"q": q & 0xF})
        # Mid changes occur AFTER sampling; carried to next row start.
        # (No mid inputs affect this design beyond reset, handled next row.)
    return out

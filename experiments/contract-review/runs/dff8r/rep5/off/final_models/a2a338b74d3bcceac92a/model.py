def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop storage. Initial value unspecified;
    # we choose 0 as a concrete placeholder (R1/R2 only constrain post-edge behavior).
    q_reg = 0

    results = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # R1_sync_reset: active high synchronous reset -> q = 0 on posedge
        # R2_d_capture: reset == 0 -> q = d on posedge
        # Both rules apply at posedge clk; reset has priority 1.
        if reset == 1:
            q_reg = 0
        else:
            q_reg = d

        results.append({"q": q_reg & 0xFF})

    return results

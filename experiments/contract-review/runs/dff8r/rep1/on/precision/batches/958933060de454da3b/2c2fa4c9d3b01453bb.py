def reference(vectors):
    # State: 8-bit D flip-flop register q_reg.
    q = 0
    current_d = 0
    current_reset = 0
    result = []

    for row in vectors:
        # Inputs driven before the sampled positive clk edge.
        if "d" in row:
            current_d = row["d"]
        if "reset" in row:
            current_reset = row["reset"]

        # r_posedge_q_sync_reset:
        # At each positive clk edge, active-high synchronous reset dominates:
        # reset==1 -> q <= 0; otherwise q <= d.
        if current_reset:
            q = 0
        else:
            q = current_d & 255

        # q is sampled after the positive edge has settled.
        result.append({"q": q})

        # Mid input changes occur AFTER sampling and are carried to the
        # start of the next vector row.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                for key in mid:
                    if key == "d":
                        current_d = mid[key]
                    elif key == "reset":
                        current_reset = mid[key]

    return result

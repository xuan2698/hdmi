def reference(vectors):
    # State: 8-bit registered output q; current nonclock inputs hold across rows.
    q = 0
    cur_d = 0
    cur_reset = 0
    result = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if "d" in row:
            cur_d = row["d"] & 255
        if "reset" in row:
            cur_reset = row["reset"] & 1

        # sync_reset_clears_q: posedge clk and reset == 1 -> q becomes 0, priority 1.
        # load_d_on_posedge_when_not_reset: posedge clk and reset == 0 -> q becomes d, priority 2.
        if cur_reset == 1:
            q = 0
        else:
            q = cur_d & 255

        # q is visible same cycle after the sampled posedge has settled.
        result.append({"q": q})

        # mid changes occur AFTER sampling and are carried to the next row.
        if "mid" in row:
            mid = row["mid"]
            if "d" in mid:
                cur_d = mid["d"] & 255
            if "reset" in mid:
                cur_reset = mid["reset"] & 1

    return result

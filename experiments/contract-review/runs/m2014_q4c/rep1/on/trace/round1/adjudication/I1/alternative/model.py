def reference(vectors):
    # Rule q_posedge_update: Implemented as negedge-triggered D flip-flop per candidate interpretation.
    # Initial state q_zero (power-up assumed 0).
    q = 0
    cur_d = 0
    cur_r = 0
    result = []
    for row in vectors:
        # Row inputs are driven before the sampled posedge.
        if "d" in row:
            cur_d = row["d"]
        if "r" in row:
            cur_r = row["r"]
        # Sample after posedge has settled; q holds for negedge-triggered FF.
        result.append({"q": q})
        # Mid changes occur after sampling, before the falling edge.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "d" in mid:
                    cur_d = mid["d"]
                if "r" in mid:
                    cur_r = mid["r"]
        # Falling edge update: if r==1 then q becomes 0; otherwise q becomes d.
        # Rule q_posedge_update: synchronous reset has priority.
        if cur_r == 1:
            q = 0
        else:
            q = cur_d
    return result

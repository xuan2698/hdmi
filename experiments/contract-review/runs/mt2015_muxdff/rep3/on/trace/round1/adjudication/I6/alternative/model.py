def reference(vectors):
    # State and registered output initialisation (power-up unspecified -> concrete 0)
    cur_L = 0
    cur_q_in = 0
    cur_r_in = 0
    Q = 0
    results = []

    for vec in vectors:
        # Drive row values before the sampled posedge
        if "L" in vec:
            cur_L = vec["L"]
        if "q_in" in vec:
            cur_q_in = vec["q_in"]
        if "r_in" in vec:
            cur_r_in = vec["r_in"]

        # load_r (priority 1): L == 1 -> load r_in on posedge clk
        if cur_L == 1:
            Q = cur_r_in & 1
        else:
            # hold_q_in (priority 2): L == 0 holds previous Q and ignores q_in
            # Candidate interpretation applied: L==0 holds the previous Q.
            Q = Q & 1

        results.append({"Q": Q & 1})

        # mid changes occur after the posedge sample and carry to the next row
        if "mid" in vec:
            mid = vec["mid"]
            if mid is not None:
                if "L" in mid:
                    cur_L = mid["L"]
                if "q_in" in mid:
                    cur_q_in = mid["q_in"]
                if "r_in" in mid:
                    cur_r_in = mid["r_in"]

    return results

def reference(vectors):
    # R_Q_POSEDGE: On posedge clk, Q updates to L ? r_in : q_in.
    # q_in is the external else-data (next-state bit), not Q feedback.
    L = 0
    q_in = 0
    r_in = 0
    Q = 0
    out = []

    for row in vectors:
        # Drive row inputs before the sampled posedge; preserve prior values if omitted.
        if "L" in row:
            L = row["L"] & 1
        if "q_in" in row:
            q_in = row["q_in"] & 1
        if "r_in" in row:
            r_in = row["r_in"] & 1

        # R_Q_POSEDGE: sample on posedge after settling.
        if L:
            Q = r_in & 1
        else:
            Q = q_in & 1

        out.append({"Q": Q & 1})

        # Optional mid changes occur after sampling and affect only the next posedge.
        if "mid" in row:
            mid = row["mid"]
            try:
                if "L" in mid:
                    L = mid["L"] & 1
                if "q_in" in mid:
                    q_in = mid["q_in"] & 1
                if "r_in" in mid:
                    r_in = mid["r_in"] & 1
            except:
                pass

    return out

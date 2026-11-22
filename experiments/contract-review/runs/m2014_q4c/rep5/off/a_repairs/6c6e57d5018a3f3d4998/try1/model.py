def reference(vectors):
    # State: Q = stored flip-flop value
    Q = 0  # power-up unspecified; choose 0

    out = []
    for row in vectors:
        d = row["d"]
        r = row["r"]

        # R1: active high synchronous reset -> q = 0 on posedge when r == 1
        # R2: D flip flop -> q = d on posedge when r == 0
        if r == 1:
            Q = 0  # R1
        else:
            Q = d & 1  # R2

        out.append({"q": Q & 1})

    return out

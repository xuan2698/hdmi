def reference(vectors):
    # Contract implementation.
    # State: Q = stored flip-flop value (initial unspecified; we pick 0 as a
    # concrete representative since output must be a concrete unsigned int).
    Q = 0  # R1/R2: initial state unspecified -> concrete 0 chosen

    out = []
    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1

        # R1: active high synchronous reset, priority 1
        # R2: D flip-flop capture when r == 0, priority 2
        # Both update at posedge clk, visible same cycle.
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        out.append({'q': Q & 1})

    return out

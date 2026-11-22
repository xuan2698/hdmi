def reference(vectors):
    # State: Q = stored flip-flop value, initializes to 0 before any clock edge
    # (candidate interpretation for global unresolved field)
    Q = 0  # R1/R2 state initialization

    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # posedge clk sampling: synchronous reset has priority
        if r == 1:
            # R1: active high synchronous reset -> q = 0
            Q = 0
        else:
            # R2: D flip flop -> q = d
            Q = d

        # Output visible same cycle
        out.append({'q': Q & 1})

        # Mid changes occur AFTER sampling, before the other edge,
        # carried to the start of the next row. Since inputs are
        # re-read each row, no extra state needed here.

    return out

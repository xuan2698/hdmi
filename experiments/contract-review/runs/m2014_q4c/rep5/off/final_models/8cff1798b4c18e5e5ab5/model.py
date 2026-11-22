def reference(vectors):
    # Contract implementation.
    # State: Q = stored flip-flop value (1 bit), power-up unspecified -> use 0.
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # posedge sampling: apply rules by priority
        # R1: r == 1 -> synchronous reset, q = 0 (priority 1)
        # R2: r == 0 -> D flip flop, q = d (priority 2)
        if r == 1:  # R1
            Q = 0
        else:       # R2
            Q = d
        out.append({'q': Q & 1})
        # mid changes occur AFTER sampling; carried to next row start.
        # (No mid handling needed here since inputs are per-row.)
    return out

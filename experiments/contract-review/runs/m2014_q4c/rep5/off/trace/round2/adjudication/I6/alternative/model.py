def reference(vectors):
    # State: Q = stored flip-flop value; initial q is 0 before any clock edge (global interpretation).
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # posedge sampling: synchronous reset has priority (R1), else load d (R2)
        if r == 1:  # R1: active high synchronous reset -> q = 0
            Q = 0
        else:       # R2: D flip flop load
            Q = d
        out.append({'q': Q & 1})
    return out

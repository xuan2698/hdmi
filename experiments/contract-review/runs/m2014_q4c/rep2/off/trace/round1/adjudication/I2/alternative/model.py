def reference(vectors):
    # State: Q (stored flip-flop value), initialized to 0 at time 0 (global interpretation)
    Q = 0
    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1
        # R1: active high synchronous reset -> q = 0 on posedge when r == 1
        # R2: D flip flop -> q = d on posedge when r == 0
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2
        out.append({'q': Q & 1})
        # mid changes occur AFTER sampling; carried to next row (no effect here
        # since we read inputs fresh each row)
    return out

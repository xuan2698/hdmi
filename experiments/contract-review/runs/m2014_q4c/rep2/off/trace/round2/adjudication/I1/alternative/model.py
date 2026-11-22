def reference(vectors):
    # State: Q = stored flip-flop value (initialized to 1 per chosen interpretation)
    Q = 1  # R-uncertain: Q initializes to 1 instead of 0

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # R1: active high synchronous reset -> q = 0 on posedge when r == 1
        # R2: D flip flop -> q = d on posedge when r == 0
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        results.append({'q': Q & 1})

    return results

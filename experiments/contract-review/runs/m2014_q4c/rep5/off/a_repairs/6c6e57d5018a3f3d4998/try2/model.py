def reference(vectors):
    # State: Q = stored flip-flop value
    Q = 0  # power-up unspecified; use 0 as concrete value

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # R1: active high synchronous reset -> q = 0 on posedge when r == 1
        # R2: r == 0 -> q = d on posedge
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        results.append({'q': Q & 1})

    return results

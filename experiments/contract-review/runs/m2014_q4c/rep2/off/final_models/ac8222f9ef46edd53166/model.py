def reference(vectors):
    # State: Q = stored flip-flop value (initial value unspecified; use 0)
    Q = 0

    results = []
    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1

        # R1: active high synchronous reset -> q = 0 on posedge
        # R2: r == 0 -> q = d on posedge
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        results.append({'q': Q & 1})

    return results

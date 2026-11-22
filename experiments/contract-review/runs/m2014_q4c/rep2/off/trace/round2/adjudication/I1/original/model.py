def reference(vectors):
    # Contract implementation.
    # State: Q = stored flip-flop value (driven to q). Initial value unspecified;
    # we choose Q=0 for concreteness (uncertain global note).
    Q = 0

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # R1: active high synchronous reset, priority 1 -> q=0 on posedge when r==1
        # R2: D flip flop, priority 2 -> q=d on posedge when r==0
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        # Output visible same cycle after posedge
        results.append({'q': Q & 1})

    return results

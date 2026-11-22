def reference(vectors):
    # Sequential 3-bit state q, 1-bit input a, sampled on posedge clk.
    # Next state: if carried a == 1 -> q = 4; else q = (q + 1) mod 8.
    # q starts unknown; first posedge resolves it.
    # Mid-cycle input changes occur after sampling and carry to next edge.
    q = None
    carried_a = None
    prev_clk = 0
    results = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        # Determine carried input: if this is the first row, initialize from a.
        # Mid changes are represented by the row's 'a' being the value driven
        # before the sampled edge; carried value updates after sampling.
        if carried_a is None:
            carried_a = a
        # Detect posedge
        if prev_clk == 0 and clk == 1:
            if carried_a == 1:
                q = 4
            else:
                if q is None:
                    q = 0
                q = (q + 1) % 8
        # After sampling, mid-cycle change: the row's a becomes carried for next edge
        # (the displayed a is driven before the edge; any mid change is carried)
        carried_a = a
        prev_clk = clk
        results.append({'q': q if q is not None else 0})
    return results

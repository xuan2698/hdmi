def reference(vectors):
    # 3-bit modulo-7 counter with synchronous load.
    # On each rising edge of clk:
    #   if sampled a == 1: q <= 4
    #   else:              q <= (q + 1) mod 7
    # Initial q is undefined (x) until first rising edge.
    #
    # Sampling convention: each row's printed 'a' is driven before the
    # sampled edge, but optional mid-interval changes occur AFTER sampling
    # and carry into the next row. So the value sampled at a posedge may
    # differ from that row's printed 'a'.
    #
    # We track the "carried" input separately from the row's printed 'a'.
    # The carried input is what will be sampled at the next posedge.

    results = []
    q = None  # undefined until first posedge
    carried_a = None  # input value that will be sampled at next posedge

    prev_clk = None

    for row in vectors:
        clk = row.get('clk')
        a = row.get('a')

        # Determine if this row represents a rising edge (posedge).
        # A posedge occurs when clk transitions from 0 to 1.
        is_posedge = (prev_clk == 0 and clk == 1)

        if is_posedge:
            # The value sampled is the carried input from before this edge.
            # If no carried value yet, use the row's printed a (first edge).
            sampled = carried_a if carried_a is not None else a
            if sampled == 1:
                q = 4
            else:
                if q is None:
                    # First posedge with a=0: q was undefined; treat as 0 then increment
                    q = 1
                else:
                    q = (q + 1) % 7
            # After sampling, mid-interval changes may occur; the row's
            # printed 'a' is the value driven before the edge, but mid
            # changes happen after sampling. For the next row, the carried
            # input is the row's printed 'a' (since mid changes are optional
            # and not explicitly given, we carry the printed a forward).
            carried_a = a
        else:
            # Not a posedge: update carried input to this row's printed a
            # (mid changes after previous sampling carry into this row).
            carried_a = a

        # Output q: if still undefined, use 0 as concrete placeholder
        out_q = q if q is not None else 0
        results.append({'q': out_q})

        prev_clk = clk

    return results

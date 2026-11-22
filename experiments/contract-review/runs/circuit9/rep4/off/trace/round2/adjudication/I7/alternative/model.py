def reference(vectors):
    # Contract implementation.
    # Rule hold_when_a_high: hold when previous a==1 (per candidate interpretation).
    # Rule increment_when_a_low: increment when previous a==0.
    # First posedge initializes q to 4 regardless of a.
    # Mid changes occur after sampling, carried to next row.

    q = None          # state: 3-bit counter, uninitialized before first posedge
    initialized = False
    prev_a = None     # previous a value used for transition decision

    results = []
    for vec in vectors:
        a = vec['a']
        # At posedge: decide transition based on prev_a (previous sampled a)
        if not initialized:
            # First posedge: load 4 regardless of a
            q = 4
            initialized = True
        else:
            if prev_a == 1:
                # hold_when_a_high: hold when previous a==1
                q = q
            else:
                # increment_when_a_low: increment when previous a==0
                q = (q + 1) & 0x7
        # Sample output after posedge settled
        results.append({'q': q})
        # Mid changes: update prev_a for next row (carried to start of next row)
        prev_a = a

    return results

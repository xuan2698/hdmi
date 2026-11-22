def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q. Initialized flag.
    # Rule hold_when_a_high: on posedge, if initialized and a==1 -> hold q.
    # Rule increment_when_a_low: on posedge, if initialized and prev_a==0 -> q = (q+1) & 7.
    # First posedge: q = 4 regardless of a (initialization).
    # Mid changes occur after sampling, carried to next row.
    # Each row: values driven before sampled posedge edge.
    # We process rows sequentially; each row corresponds to one posedge sample.
    # prev_a tracks the a value from the previous row (carried through mid changes).

    q = None
    initialized = False
    prev_a = None
    results = []

    for row in vectors:
        a = row['a']
        # At posedge sampling:
        if not initialized:
            # First posedge: load 4 regardless of a
            q = 4
            initialized = True
        else:
            # hold_when_a_high: if a==1, hold
            if a == 1:
                pass  # hold q
            else:
                # increment_when_a_low: prev_a == 0 -> increment
                if prev_a == 0:
                    q = (q + 1) & 7
                # else hold (prev_a == 1 and a == 0 -> hold)
        results.append({'q': q})
        # After sampling, mid changes may occur; a is carried to next row.
        prev_a = a

    return results

def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q.
    # Rule global: q initializes to 4 via implicit power-on value.
    # Rule hold_when_a_high: on posedge, if a==1 (and initialized), hold q.
    # Rule increment_when_a_low: on posedge, if prev_a==0, increment q (mod 8).
    # First posedge: q loads 4 regardless of a (initialization).
    # Mid changes occur after sampling, carried to next row.

    q = 4  # global: implicit power-on value
    initialized = False
    prev_a = None
    results = []

    for row in vectors:
        a = row['a']
        # posedge sampling
        if not initialized:
            # first posedge loads 4 regardless of a
            q = 4
            initialized = True
        else:
            if prev_a == 0:
                # increment_when_a_low
                q = (q + 1) & 0x7
            else:
                # hold_when_a_high
                q = q
        results.append({'q': q})
        # mid changes: update prev_a after sampling for next cycle
        prev_a = a

    return results

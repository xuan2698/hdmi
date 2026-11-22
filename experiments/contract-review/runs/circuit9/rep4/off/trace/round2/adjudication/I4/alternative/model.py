def reference(vectors):
    # Contract implementation.
    # State: q (3-bit counter), initialized flag.
    # Rule hold_when_a_high: on posedge, if initialized and prev_a==1, hold q.
    # Rule increment_when_a_low: on posedge, if prev_a==0, increment q mod 8.
    # First posedge: q loads 4 regardless of a (initialization).
    # Mid changes occur after sampling, carried to next row.

    q = 0
    initialized = False
    prev_a = 0
    out = []

    for vec in vectors:
        a = vec.get('a', 0)
        # posedge sampling
        if not initialized:
            # first posedge loads 4 regardless of a
            q = 4
            initialized = True
        else:
            if prev_a == 0:
                # increment_when_a_low: wrap modulo 8
                q = (q + 1) % 8
            else:
                # hold_when_a_high
                q = q
        out.append({'q': q & 0x7})
        # mid changes: a carried to next row as prev_a
        prev_a = a

    return out

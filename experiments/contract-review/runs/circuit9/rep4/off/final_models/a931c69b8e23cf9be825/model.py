def reference(vectors):
    # Contract implementation.
    # State: count (3-bit). Power-on value 4 (candidate interpretation for global uncertainty).
    # Rule hold_when_a_high: on posedge, if a==1 and initialized -> hold q.
    # Rule increment_when_a_low: on posedge, if a==0 and initialized -> q = (q+1) mod 8.
    # First posedge: q loads 4 regardless of a (initialization).
    # Mid changes occur after sampling, carried to next row.

    q = 4  # power-on value per candidate interpretation
    initialized = False
    out = []

    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling
        if not initialized:
            # first posedge loads 4 regardless of a
            q = 4
            initialized = True
        else:
            if a == 1:
                # hold_when_a_high
                q = q
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q & 0x7})
        # mid changes (if any) would be applied here after sampling;
        # they are carried to next row via row dict already containing them.
    return out

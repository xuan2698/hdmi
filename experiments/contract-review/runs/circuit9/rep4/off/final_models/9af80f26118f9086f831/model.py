def reference(vectors):
    # Contract implementation.
    # State: q (3-bit counter), initialized flag.
    # Rules:
    #   hold_when_a_high: on posedge, if a==1 and initialized, q holds.
    #   increment_when_a_low: on posedge, if a==0 and initialized, q = (q+1) & 7.
    #   First posedge: q loads 4 regardless of a (initialization).
    #   Before first posedge: q is x (we output 0 as concrete unsigned).
    # Mid changes occur after sampling, carried to next row.

    q = 0
    initialized = False
    results = []

    for row in vectors:
        a = row.get('a', 0)
        # Posedge sampling occurs here (each row represents a posedge sample).
        if not initialized:
            # First posedge: load 4 regardless of a.
            q = 4
            initialized = True
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        results.append({'q': q & 0x7})
        # Mid changes (if any) would be applied here after sampling;
        # they affect 'a' for the next row, which is already reflected
        # in the next row's 'a' value.

    return results

def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments by 1 (priority 2)
    # Initialization: q initializes to 4 at the first posedge (from x).
    #   So on the very first posedge, regardless of a, q becomes 4.
    #   After that, normal rules apply.
    # State: q (3-bit counter), initialized to None (x) before first posedge.
    q = None
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge update
        if q is None:
            # First posedge: initialize to 4 (rule: global init)
            q = 4
        else:
            if a == 1:
                # hold_when_a_high (priority 1)
                q = q
            else:
                # increment_when_a_low (priority 2)
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out

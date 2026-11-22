def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 2)
    # No reset. Initial q unspecified; use 4 as initialization at first posedge
    # (selected interpretation: q initializes to 4 at first posedge regardless of a).
    # Mid changes: none.
    q = None  # unspecified before first posedge
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge sampling
        if q is None:
            # first posedge: initialize to 4 regardless of a
            q = 4
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out

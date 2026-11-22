def reference(vectors):
    # State: q is the 3-bit counter value. Initial value is unspecified (x) until
    # the first posedge, at which point q initializes to 4 regardless of a.
    # Rule global: q initializes to 4 at the first posedge regardless of a.
    # Rule hold_when_a_high: on posedge with a==1, q holds.
    # Rule increment_when_a_low: on posedge with a==0, q increments (mod 8).
    q = None  # unspecified before first posedge
    first_edge = True
    out = []
    for row in vectors:
        a = row['a']
        # posedge sampling: apply transition
        if first_edge:
            # global: initialize to 4 at first posedge regardless of a
            q = 4
            first_edge = False
        else:
            if a == 1:
                # hold_when_a_high
                q = q
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out

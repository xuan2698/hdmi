def reference(vectors):
    # Contract implementation.
    # State: count (3-bit), initializes to 4 at first posedge (from x).
    # Rule hold_when_a_high (priority 1): when a==1 at posedge, q holds.
    # Rule increment_when_a_low (priority 2): when a==0 at posedge, q increments mod 8.
    # Global interpretation: q initialized to 4 at first posedge.

    q = None  # unspecified until first posedge
    prev_a = None
    out = []

    for vec in vectors:
        a = vec.get('a', 0)
        # posedge sampling: compute next state
        if q is None:
            # global: initialize to 4 at first posedge
            q = 4
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) % 8
        prev_a = a
        out.append({'q': q & 0x7})

    return out

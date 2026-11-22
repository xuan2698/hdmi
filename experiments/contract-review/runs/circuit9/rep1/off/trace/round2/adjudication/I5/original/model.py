def reference(vectors):
    # Contract implementation.
    # State: count (3-bit), initializes to 4 at first posedge (from x).
    # Rule hold_when_a_high (priority 1): on posedge, if a==1, q holds.
    # Rule increment_when_a_low (priority 2): on posedge, if a==0, q increments
    #   (mod 8), except the special case where q==4 and previous_a==1 -> hold.
    # "previous_a" refers to the a value at the prior posedge (the value that
    # produced the current q). At first posedge, q initializes to 4 regardless.

    q = None          # unknown until first posedge
    prev_a = None     # a value at previous posedge (None before first)
    initialized = False

    out = []
    for row in vectors:
        a = row['a']
        # posedge sampling: compute next q
        if not initialized:
            # First posedge: initialize count to 4 (from x)
            q = 4
            initialized = True
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low, with exception q==4 and prev_a==1
                if q == 4 and prev_a == 1:
                    pass
                else:
                    q = (q + 1) & 0x7
        prev_a = a
        out.append({'q': q})
    return out

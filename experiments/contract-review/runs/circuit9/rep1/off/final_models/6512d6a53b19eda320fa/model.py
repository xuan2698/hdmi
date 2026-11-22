def reference(vectors):
    # Contract implementation.
    # State: count = 3-bit counter stored in q.
    # Initialization: q initializes to 4 at time 0 (per resolved global interpretation).
    # Rule hold_when_a_high (priority 1): on posedge, if a==1, q holds.
    # Rule increment_when_a_low (priority 2): on posedge, if a==0, q increments by 1 (mod 8).
    # No reset. No mid-cycle changes.

    q = 4  # global: q initializes to 4 at time 0
    out = []
    for row in vectors:
        a = row["a"]
        # posedge update
        if a == 1:
            # hold_when_a_high
            q = q
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({"q": q & 0x7})
    return out

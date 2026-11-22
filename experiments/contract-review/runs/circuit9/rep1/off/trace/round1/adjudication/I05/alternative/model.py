def reference(vectors):
    # Contract implementation.
    # State: count = 3-bit counter stored in q.
    # Rule global: q initializes to 4 at the first posedge regardless of a.
    # Rule hold_when_a_high: on posedge, if a==1, q holds.
    # Rule increment_when_a_low: on posedge, if a==0, q increments (mod 8).
    # No reset. Mid changes: none.
    # Each row's values are driven before the sampled posedge.
    # We process each vector as one posedge sample.

    q = None  # power-up unspecified
    first = True
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge update
        if first:
            # global: initialize to 4 at first posedge regardless of a
            q = 4
            first = False
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out

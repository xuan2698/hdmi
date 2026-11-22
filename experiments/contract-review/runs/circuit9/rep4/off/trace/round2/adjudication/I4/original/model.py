def reference(vectors):
    # State: q (3-bit), initialized flag, prev_a
    # Rule hold_when_a_high / increment_when_a_low: on posedge, if not initialized -> q=4, initialized=True
    # else if prev_a == 0 -> q = (q+1) & 7, else hold.
    # prev_a is the a value sampled at the previous posedge (i.e., "previous a").
    q = 0
    initialized = False
    prev_a = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge sampling
        if not initialized:
            q = 4
            initialized = True
        else:
            if prev_a == 0:
                q = (q + 1) & 7
            # else hold
        prev_a = a
        out.append({'q': q})
    return out

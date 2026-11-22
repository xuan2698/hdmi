def reference(vectors):
    # Contract implementation.
    # State: 3-bit accumulator q, previous sampled a (prev_a).
    # Initial q is unspecified; use 0 as concrete value (uncertain global).
    q = 0
    prev_a = None  # no previous sample yet

    results = []
    for vec in vectors:
        a = vec["a"]
        # posedge sampling: compute next q based on current a and prev_a
        # Rule hold_when_a_high: a==1 or prev_a==0 -> hold
        # Rule increment_when_a_low: a==0 and prev_a==1 -> increment
        if prev_a is not None and a == 0 and prev_a == 1:
            # increment_when_a_low
            q = (q + 1) & 0x7
        else:
            # hold_when_a_high
            q = q & 0x7
        prev_a = a
        results.append({"q": q})
    return results

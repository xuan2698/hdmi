def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1 or previous a==0, q holds.
    # increment_when_a_low: on posedge, if a==0 and previous a==1, q increments by 1.
    # Initial q is unspecified; choose 4 to match contract examples (q starts at 4).
    # State: count (3-bit accumulator), prev_a (previous sampled a).
    # No reset. Mid changes: none.
    q = 4  # initial unspecified; selected to satisfy contract examples
    prev_a = 1  # initial previous a assumed 1 (matches first example: a=1 holds q=4)
    out = []
    for v in vectors:
        a = v['a']
        # posedge sampling: apply transition based on current a and prev_a
        if a == 0 and prev_a == 1:
            # increment_when_a_low
            q = (q + 1) & 0x7
        else:
            # hold_when_a_high
            q = q & 0x7
        prev_a = a
        out.append({'q': q})
    return out

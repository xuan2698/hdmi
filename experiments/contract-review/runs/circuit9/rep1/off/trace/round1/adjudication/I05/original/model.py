def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 2)
    # No reset; power-up unspecified -> use 0 as concrete initial value.
    q = 0
    out = []
    for v in vectors:
        a = v["a"]
        # posedge update
        if a == 1:  # hold_when_a_high
            q = q
        else:  # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({"q": q})
    return out

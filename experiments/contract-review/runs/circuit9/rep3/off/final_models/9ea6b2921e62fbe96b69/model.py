def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds.
    # increment_when_a_low: on posedge, if a==0, q increments (3-bit wrap 7->0).
    # Initial q = 4 at time 0 (no reset).
    # Sample after posedge has settled. Mid changes occur after sampling,
    # before the other edge, carried to start of next row.
    q = 4
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge sampling: apply transition based on current a
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low (3-bit wrap)
            q = (q + 1) & 0x7
        out.append({'q': q})
    return out

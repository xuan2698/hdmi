def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8)
    # Initial q = 4 (no reset). First posedge with a=1 loads 4 (already 4).
    # Mid changes occur after sampling, before next edge; carried to next row.
    q = 4
    out = []
    for vec in vectors:
        a = vec.get('a', 0)
        # posedge sampling: apply transition based on current a
        if a == 1:
            # hold_when_a_high
            q = q
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q})
        # mid changes (if any) would be applied here after sampling;
        # none specified in vectors, so nothing to do.
    return out

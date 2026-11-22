def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds.
    # increment_when_a_low: on posedge, if a==0, q increments (mod 8).
    # Initial q = 4 (no reset).
    # Each row: values driven before sampled posedge; sample after posedge settles.
    # Mid changes occur AFTER sampling, carried to next row start.
    q = 4
    out = []
    for row in vectors:
        a = row['a']
        # posedge sampling: apply transition based on a
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q})
        # mid changes (if any) occur after sampling; carried to next row.
        # No mid keys specified in contract beyond generic note; nothing to apply.
    return out

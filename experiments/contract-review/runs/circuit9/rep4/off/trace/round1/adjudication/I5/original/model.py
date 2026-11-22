def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 1)
    # reset: none; power-up unspecified -> use 0 as concrete initial value
    # mid changes occur AFTER sampling, before other edge, carried to next row
    q = 0  # power-up unspecified; concrete choice
    out = []
    for row in vectors:
        a = row["a"]
        # posedge sampling: apply transition based on a
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({"q": q})
        # mid changes (if any) occur after sampling; they affect next row's a,
        # which is already provided in the next vector row, so nothing to do here.
    return out

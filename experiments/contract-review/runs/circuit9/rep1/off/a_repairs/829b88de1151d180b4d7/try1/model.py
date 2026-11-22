def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 2)
    # state: count (3-bit), no reset; power-up unspecified -> use 0 as concrete start
    # Each row: values driven before sampled posedge; sample after posedge settles.
    # Return dict per row with q as unsigned int in [0,7].

    q = 0  # concrete power-up value (unspecified in spec; choose 0)
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge update
        if a == 1:
            # hold_when_a_high
            q = q & 0x7
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q})
    return out

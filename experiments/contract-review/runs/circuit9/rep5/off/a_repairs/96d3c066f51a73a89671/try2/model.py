def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8)
    # reset: none. Power-up unspecified; use 0 as concrete initial value.
    # State: count (3-bit accumulator), update_time posedge.
    # Sample after posedge has settled; each row's values driven before sampled edge.
    # No mid changes.

    q = 0  # power-up unspecified -> concrete 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge update
        if a == 1:
            # hold_when_a_high
            q = q
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q & 0x7})
    return out

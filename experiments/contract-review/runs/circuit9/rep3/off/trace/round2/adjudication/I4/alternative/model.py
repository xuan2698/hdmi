def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q. Power-up unspecified (x). Per candidate interpretation
    # for the unresolved global rule: q starts x; on the first posedge with a=1,
    # q becomes 4 (load), then holds while a=1. When a=0, q increments by 1.
    # Rule hold_when_a_high: a==1 -> q holds (after initial load of 4).
    # Rule increment_when_a_low: a==0 -> q = (q+1) mod 8.
    # Mid input changes occur AFTER sampling, before the other edge, and are
    # carried to the start of the next row.

    q = None  # unspecified power-up value
    loaded = False  # whether the initial load of 4 has occurred
    out = []

    for row in vectors:
        a = row.get('a')
        # Sample at posedge (values driven before the sampled edge).
        if a == 1:
            # hold_when_a_high (priority 1)
            if not loaded:
                # candidate interpretation: first posedge with a=1 loads 4
                q = 4
                loaded = True
            # else hold q unchanged
        else:
            # increment_when_a_low (priority 1)
            if not loaded:
                # q is unspecified; treat as 0 for concrete output, then increment
                q = 0
                loaded = True
            q = (q + 1) % 8

        out.append({'q': q})

        # Mid changes: applied after sampling, carried to next row.
        # (No explicit mid fields in this contract; nothing to apply.)

    return out

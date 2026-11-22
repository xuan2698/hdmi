def reference(vectors):
    # State: q (3-bit counter), prev_a (previous value of a)
    # Rule hold_when_a_high: at posedge, if a==1, q holds.
    # Rule increment_when_a_low: at posedge, if a==0, q increments by 1,
    #   except the special case where q==4 and previous_a==1 (first posedge
    #   after a high period) — then q holds at 4.
    # Global interpretation: first posedge unconditionally sets q=4.
    #   prev_a initialized to 0 (don't care) for first cycle.

    q = None          # unknown until first posedge
    prev_a = 0        # initialized for first cycle (global interpretation)
    first_edge = True

    results = []
    for vec in vectors:
        a = vec['a'] & 1  # 1-bit input

        # Posedge update
        if first_edge:
            # global: first posedge unconditionally sets q=4
            q = 4
            first_edge = False
        else:
            if a == 1:
                # hold_when_a_high: q holds
                pass
            else:
                # increment_when_a_low: q increments, except q==4 and prev_a==1
                if q == 4 and prev_a == 1:
                    pass  # hold at 4
                else:
                    q = (q + 1) & 0x7  # 3-bit wrap

        prev_a = a
        results.append({'q': q & 0x7})

    return results

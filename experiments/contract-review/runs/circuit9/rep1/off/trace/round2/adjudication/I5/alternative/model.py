def reference(vectors):
    # State: q is the 3-bit counter value; initializes to 4 at first posedge (from x).
    # previous_a is the value of a at the previous posedge (registered).
    # Rule hold_when_a_high: when a==1 at posedge, q holds.
    # Rule increment_when_a_low: when a==0 at posedge, q increments by 1 (mod 8),
    #   except the special case where q==4 and previous_a==1 (the first transition
    #   from a=1 to a=0 does not increment; it just holds at 4).
    # We use the registered previous_a interpretation.

    q = None          # unspecified until first posedge
    previous_a = None # no previous posedge yet
    out = []

    for row in vectors:
        a = row['a']
        clk = row.get('clk', 1)  # each row represents a posedge sample

        # Compute next state at posedge
        if q is None:
            # First posedge: initialize to 4 (rule: initializes to 4 at first posedge)
            q = 4
        else:
            if a == 1:
                # hold_when_a_high (priority 1)
                pass
            else:  # a == 0
                # increment_when_a_low (priority 2), with special case
                if q == 4 and previous_a == 1:
                    # special: first transition from a=1 to a=0 holds at 4
                    pass
                else:
                    q = (q + 1) % 8

        # Register a for next cycle
        previous_a = a

        out.append({'q': q})

    return out

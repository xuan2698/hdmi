def reference(vectors):
    # State: 3-bit counter value stored in q.
    # Initializes to 4 on first posedge regardless of a.
    # Then increments by 1 on each posedge when previous a=0, holds when previous a=1.
    # Rule hold_when_a_high (priority 1): a==1 && initialized -> hold q.
    # Rule increment_when_a_low: prev_a==0 -> increment q (mod 8).
    # First posedge loads 4 unconditionally (per unresolved interpretation).
    # Mid input changes occur AFTER sampling, carried to start of next row.
    # We track prev_a as the a value seen at the previous posedge sample.
    q = None  # unspecified before first posedge
    initialized = False
    prev_a = None
    results = []
    for row in vectors:
        a = row['a']
        # At posedge: sample using prev_a (a from previous cycle) for increment/hold decision.
        if not initialized:
            # First posedge: load 4 unconditionally
            q = 4
            initialized = True
        else:
            if prev_a == 0:
                # increment_when_a_low
                q = (q + 1) & 0x7
            else:
                # hold_when_a_high
                q = q
        # After sampling, mid changes may occur; a becomes prev_a for next cycle.
        prev_a = a
        results.append({'q': q})
    return results

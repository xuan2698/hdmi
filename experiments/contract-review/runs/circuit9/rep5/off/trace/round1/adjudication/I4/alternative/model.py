def reference(vectors):
    # State: 3-bit accumulator q, initialized to 4 (from power-up observation at first posedge)
    # Rule hold_when_a_high: on posedge, if a==1, q holds.
    # Rule increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8).
    #   Candidate interpretation: increment only on posedge where a=0 AND previous sampled a=1; hold otherwise.
    #   We follow the candidate interpretation as instructed.
    # No reset. Mid changes: none.
    q = 4
    prev_a = 1  # previous sampled a value; initial a=1 at time 0
    out = []
    for v in vectors:
        a = v['a']
        # posedge sampling: apply transition based on current a and prev_a
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low (candidate interpretation: only if prev_a==1)
            if prev_a == 1:
                q = (q + 1) % 8
            # else hold
        prev_a = a
        out.append({'q': q})
    return out

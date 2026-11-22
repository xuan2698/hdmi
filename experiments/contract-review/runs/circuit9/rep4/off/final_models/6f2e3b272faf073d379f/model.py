def reference(vectors):
    # State: q (3-bit), prev_a (sampled at previous posedge), first (first posedge flag)
    # Rule load_on_first_posedge (priority 0): first posedge loads 4 regardless of a
    # Rule hold_when_a_high (priority 1): if current a == 1 at posedge, hold q
    # Rule increment_when_a_low (priority 1): if current a == 0 at posedge, increment q (mod 8)
    # Per candidate interpretation: increment iff current a == 0 at posedge (not previous sampled a)
    q = 0
    first = True
    out = []
    for row in vectors:
        a = row['a']
        # posedge sampling: compute next q
        if first:
            # load_on_first_posedge
            q = 4
            first = False
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out

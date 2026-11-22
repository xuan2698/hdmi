def reference(vectors):
    # Contract rules implemented:
    # load_on_first_posedge: first posedge after start loads q=4 regardless of a
    # hold_when_a_high: on posedge, if prev_a == 1, hold q
    # increment_when_a_low: on posedge, if prev_a == 0, increment q (mod 8)
    # prev_a is the value of a sampled at the previous posedge (delayed a).
    # Initial prev_a is treated as 1 so first posedge loads 4 (priority 0).
    # Mid changes occur after sampling, carried to next row.

    q = None          # state: 3-bit counter value
    prev_a = 1        # delayed a; initial 1 so first posedge loads 4
    first = True      # first posedge flag
    out = []

    for row in vectors:
        a = row['a']
        # posedge sampling: use prev_a (delayed a) for decision
        if first:
            # load_on_first_posedge (priority 0)
            q = 4
            first = False
        else:
            if prev_a == 1:
                # hold_when_a_high (priority 1)
                pass
            else:
                # increment_when_a_low (priority 1)
                q = (q + 1) & 0x7
        # update delayed a with current sampled a for next posedge
        prev_a = a
        out.append({'q': q & 0x7})
    return out

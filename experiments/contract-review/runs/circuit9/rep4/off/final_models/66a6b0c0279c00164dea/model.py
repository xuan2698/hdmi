def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q, plus prev_a (a sampled at previous posedge).
    # Rule load_on_first_posedge (priority 0): first posedge loads 4 regardless of a.
    # Rule hold_when_a_high (priority 1): if prev_a == 1, hold q.
    # Rule increment_when_a_low (priority 1): if prev_a == 0, q = (q + 1) & 7.
    # Uncertain global interpretation: increment iff prev_a == 0; first posedge loads 4.
    # Mid changes occur after sampling, carried to next row.

    q = None          # power-up unspecified
    prev_a = None     # no previous sample yet
    first = True      # first posedge flag
    out = []

    for row in vectors:
        a = row['a']
        # posedge sampling: use prev_a (delayed a) for decision
        if first:
            # load_on_first_posedge
            q = 4
            first = False
        else:
            if prev_a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 7
        # record output for this row (concrete unsigned int in 3 bits)
        out.append({'q': q & 7})
        # after sampling, mid changes: update prev_a to current a for next row
        prev_a = a

    return out

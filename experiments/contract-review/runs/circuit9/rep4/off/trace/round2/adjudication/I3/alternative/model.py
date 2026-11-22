def reference(vectors):
    # Contract implementation.
    # State: count (3-bit), implicit power-on value 4 (per unresolved-field interpretation).
    # Rule hold_when_a_high: on posedge, if prev_a == 1, hold q.
    # Rule increment_when_a_low: on posedge, if prev_a == 0, q = (q + 1) & 7.
    # prev_a is the value of a sampled at the previous posedge (initially 1, since
    # the first posedge at 5ns holds q=4 with a=1 -> consistent with prev_a=1).
    # Mid changes occur after sampling and carry to next row; we sample a at each
    # posedge (row) and use it as prev_a for the next posedge.

    q = 4          # implicit power-on value (rule: global interpretation)
    prev_a = 1     # first posedge holds (a=1 at 5ns), so prev_a starts as 1
    out = []

    for row in vectors:
        a = row["a"]
        # posedge sampling: use prev_a to decide transition
        if prev_a == 1:
            # hold_when_a_high
            q = q & 7
        else:
            # increment_when_a_low
            q = (q + 1) & 7
        # current a becomes prev_a for next posedge (mid changes carry over)
        prev_a = a
        out.append({"q": q})

    return out

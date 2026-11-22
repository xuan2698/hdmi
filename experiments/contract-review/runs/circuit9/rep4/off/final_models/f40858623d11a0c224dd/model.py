def reference(vectors):
    # Rule IDs implemented:
    # load_on_first_posedge: first posedge after start loads q=4
    # hold_when_a_high: on posedge, if current a==1, hold q
    # increment_when_a_low: on posedge, if current a==0, q = (q+1) mod 8
    # global (resolved): increment iff current a == 0; first posedge loads 4
    q = None
    first = True
    out = []
    for v in vectors:
        a = v.get('a', 0)
        # posedge sampling: each row represents a posedge sample
        if first:
            q = 4  # load_on_first_posedge
            first = False
        else:
            if a == 1:
                pass  # hold_when_a_high
            else:
                q = (q + 1) & 0x7  # increment_when_a_low
        out.append({'q': q})
    return out

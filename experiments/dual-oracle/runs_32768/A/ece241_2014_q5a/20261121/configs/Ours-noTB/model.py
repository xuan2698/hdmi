def reference(vectors):
    state = 0
    outs = []
    zmap = (0, 1, 1, 0)
    for v in vectors:
        if v.get('areset', 0):
            state = 0
        else:
            x = v.get('x', 0) & 1
            if state == 0:
                state = 1 if x else 0
            else:
                state = 2 if x == 0 else 3
        outs.append({'z': zmap[state]})
    return outs

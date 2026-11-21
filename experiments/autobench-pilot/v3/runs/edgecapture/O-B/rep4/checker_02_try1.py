def reference(vectors):
    out = []
    state = 0
    prev_in = 0
    for row in vectors:
        reset = row.get('reset', 0)
        inp = row.get('in', 0)
        if reset:
            state = 0
        else:
            state |= prev_in & ~inp
        out.append({'out': state & 0xFFFFFFFF})
        prev_in = inp
        if 'mid' in row:
            mid = row['mid']
            if mid.get('reset', 0):
                state = 0
            if 'in' in mid:
                inp2 = mid['in']
                if not mid.get('reset', 0):
                    state |= prev_in & ~inp2
                prev_in = inp2
    return out

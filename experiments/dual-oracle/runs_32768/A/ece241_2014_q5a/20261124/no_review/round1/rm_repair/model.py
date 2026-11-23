def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        if int(row['areset']):
            state = 0
            z = 0
        else:
            x = int(row['x'])
            if state == 0:
                if x:
                    state = 1
                else:
                    state = 0
            else:
                if x:
                    state = 2
                else:
                    state = 1
            z = 1 if state == 1 else 0
        out.append({'z': z})
        mid = row.get('mid')
        if mid is not None:
            if 'areset' in mid and int(mid['areset']):
                state = 0
    return out

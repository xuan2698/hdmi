def reference(vectors):
    out = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        if y == 0:
            nxt = 0 if x == 0 else 1
        elif y == 1:
            nxt = 1 if x == 0 else 4
        elif y == 2:
            nxt = 2 if x == 0 else 1
        elif y == 3:
            nxt = 1 if x == 0 else 2
        elif y == 4:
            nxt = 3 if x == 0 else 4
        else:
            nxt = 0
        Y0 = nxt & 1
        z = 1 if (y == 3 or y == 4) else 0
        out.append({'Y0': Y0, 'z': z})
    return out

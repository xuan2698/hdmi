def reference(vectors):
    out = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        if y == 0:
            Y = 1 if x else 0
        elif y == 1:
            Y = 4 if x else 1
        elif y == 2:
            Y = 1 if x else 2
        elif y == 3:
            Y = 2 if x else 1
        elif y == 4:
            Y = 4 if x else 3
        else:
            Y = 0
        Y0 = Y & 1
        z = 1 if (y == 3 or y == 4) else 0
        out.append({'Y0': Y0, 'z': z})
    return out

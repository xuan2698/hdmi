def reference(vectors):
    out = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        if y == 0:
            Y = 1 if x else 0
            z = 0
        elif y == 1:
            Y = 4 if x else 1
            z = 0
        elif y == 2:
            Y = 1 if x else 2
            z = 0
        elif y == 3:
            Y = 2 if x else 1
            z = 1
        elif y == 4:
            Y = 4 if x else 3
            z = 1
        else:
            Y = 0
            z = 0
        out.append({'Y0': Y & 1, 'z': z & 1})
    return out

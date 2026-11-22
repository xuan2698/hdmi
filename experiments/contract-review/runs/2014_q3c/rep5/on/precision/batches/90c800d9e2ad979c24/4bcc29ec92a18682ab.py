def reference(vectors):
    out = []
    for v in vectors:
        x = v.get('x', 0)
        y = v.get('y', 0)
        Y0 = 0
        if y < 5:
            if (x == 0 and (y == 1 or y == 3 or y == 4)) or (x == 1 and (y == 0 or y == 2)):
                Y0 = 1
        if y == 3 or y == 4:
            z = 1
        else:
            z = 0
        out.append({'Y0': Y0, 'z': z})
    return out
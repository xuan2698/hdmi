def reference(vectors):
    table = {
        0: (0, 1, 0),
        1: (1, 0, 0),
        2: (0, 1, 0),
        3: (1, 0, 1),
        4: (1, 0, 1),
    }
    out = []
    for v in vectors:
        x = v['x']
        y = v['y']
        n0, n1, z = table.get(y, (0, 0, 0))
        out.append({'Y0': n1 if x else n0, 'z': z})
    return out

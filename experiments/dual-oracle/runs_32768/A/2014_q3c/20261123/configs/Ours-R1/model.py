def reference(vectors):
    out = []
    for r in vectors:
        x = int(r['x'])
        y = int(r['y'])
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1
        Y0 = ((y2 | y0) ^ x) & 1
        z = (y2 | (y1 & y0)) & 1
        out.append({'Y0': Y0, 'z': z})
    return out

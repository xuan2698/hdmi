def reference(vectors):
    out = []
    for v in vectors:
        x = v['x']
        y = v['y']
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1
        nx = 1 - x
        Y0 = ((nx & y0) | (nx & y2) | (x & (1 - y2) & (1 - y0))) & 1
        z = (y2 | (y1 & y0)) & 1
        out.append({'Y0': Y0, 'z': z})
    return out
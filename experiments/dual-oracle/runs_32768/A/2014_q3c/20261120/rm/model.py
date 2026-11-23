def reference(vectors):
    out = []
    for v in vectors:
        x = v['x']
        y = v['y']
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1
        out.append({
            'Y0': x ^ (y2 | y0),
            'z': y2 | (y1 & y0)
        })
    return out

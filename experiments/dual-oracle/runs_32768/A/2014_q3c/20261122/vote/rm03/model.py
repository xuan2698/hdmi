def reference(vectors):
    out = []
    for row in vectors:
        x = row['x']
        y = row['y']
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1
        Y0 = (x ^ y0) if y2 == 0 else (1 - x)
        z = y2 | (y1 & y0)
        out.append({'Y0': int(Y0) & 1, 'z': int(z) & 1})
    return out

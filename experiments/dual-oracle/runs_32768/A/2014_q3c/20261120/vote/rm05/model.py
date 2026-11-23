def reference(vectors):
    out = []
    for row in vectors:
        if isinstance(row, dict):
            x = row['x']
            y = row['y']
        else:
            x, y = row
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1
        Y0 = (x ^ y0 ^ y2) & 1
        z = (y2 | (y1 & y0)) & 1
        out.append({'Y0': Y0, 'z': z})
    return out

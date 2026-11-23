def reference(vectors):
    result = []
    for row in vectors:
        x = row['x']
        y = row['y']
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1
        Y0 = (((1 - x) & y0) | ((1 - x) & y2) | (x & (1 - y2) & (1 - y0))) & 1
        z = (y2 | (y1 & y0)) & 1
        result.append({'Y0': Y0, 'z': z})
    return result

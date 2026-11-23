def reference(vectors):
    result = []
    for row in vectors:
        x = row['x'] & 1
        y = row['y'] & 7
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1
        Y0 = ((1 - x) & (y0 | y2)) | (x & (1 - y2) & (1 - y0))
        z = y2 | (y1 & y0)
        result.append({'Y0': Y0 & 1, 'z': z & 1})
    return result

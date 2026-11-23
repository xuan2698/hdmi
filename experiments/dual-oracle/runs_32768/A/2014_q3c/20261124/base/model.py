def reference(vectors):
    x = 0
    y = 0
    res = []
    for row in vectors:
        if 'x' in row:
            x = row['x'] & 1
        if 'y' in row:
            y = row['y'] & 7
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1
        Y0 = (x ^ y0 ^ y2) & 1
        z = (y1 & y0) | ((1 ^ y1) & y2)
        z = z & 1
        res.append({'Y0': Y0, 'z': z})
        if 'mid' in row:
            mid = row['mid']
            if 'x' in mid:
                x = mid['x'] & 1
            if 'y' in mid:
                y = mid['y'] & 7
    return res

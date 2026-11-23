def reference(vectors):
    result = []
    for row in vectors:
        x = row['x'] & 1
        y = row['y'] & 7
        a = (y >> 2) & 1
        b = (y >> 1) & 1
        c = y & 1
        xp = 1 - x
        Y0 = (a & xp) | (c & xp) | ((1 - a) & (1 - c) & x)
        z = a | (b & c)
        result.append({'Y0': Y0, 'z': z})
    return result

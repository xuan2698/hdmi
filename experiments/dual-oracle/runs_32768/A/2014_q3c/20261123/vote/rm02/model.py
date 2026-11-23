def reference(vectors):
    result = []
    for row in vectors:
        if isinstance(row, dict):
            x = row['x'] & 1
            y = row['y'] & 7
        else:
            x = row[0] & 1
            y = row[1] & 7
        a = (y >> 2) & 1
        b = (y >> 1) & 1
        c = y & 1
        Y0 = ((a | c) ^ x) & 1
        z = (a | (b & c)) & 1
        result.append({'Y0': Y0, 'z': z})
    return result

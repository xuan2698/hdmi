def reference(vectors):
    out = []
    for row in vectors:
        x = row['x'] & 1
        y = row['y'] & 7
        if y == 0:
            y0 = x
        elif y == 1:
            y0 = 1 ^ x
        elif y == 2:
            y0 = x
        elif y == 3:
            y0 = 1 ^ x
        elif y == 4:
            y0 = 1 ^ x
        else:
            y0 = 0
        z = 1 if y == 3 or y == 4 else 0
        out.append({'Y0': y0 & 1, 'z': z})
    return out

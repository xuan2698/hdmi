def reference(vectors):
    out = []
    for row in vectors:
        x = row['x'] & 1
        y = row['y'] & 7
        if y == 0:
            Y0 = x
            z = 0
        elif y == 1:
            Y0 = 1 if x == 0 else 0
            z = 0
        elif y == 2:
            Y0 = x
            z = 0
        elif y == 3:
            Y0 = 1 if x == 0 else 0
            z = 1
        elif y == 4:
            Y0 = 1 if x == 0 else 0
            z = 1
        else:
            Y0 = 0
            z = 0
        out.append({'Y0': Y0, 'z': z})
    return out

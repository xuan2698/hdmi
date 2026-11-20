def reference(vectors):
    results = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1

        if y == 0:
            Y = 1 if x else 0
            z = 0
        elif y == 1:
            Y = 4 if x else 1
            z = 0
        elif y == 2:
            Y = 1 if x else 2
            z = 0
        elif y == 3:
            Y = 2 if x else 1
            z = 1
        elif y == 4:
            Y = 4 if x else 3
            z = 1
        else:
            Y = 0
            z = 0

        Y0 = Y & 1
        results.append({'Y0': Y0, 'z': z})
    return results

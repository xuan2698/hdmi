def reference(vectors):
    result = []
    for row in vectors:
        x = int(row['x']) & 1
        y = int(row['y']) & 7

        if y == 0:
            Y0 = x
            z = 0
        elif y == 1:
            Y0 = 1 - x
            z = 0
        elif y == 2:
            Y0 = x
            z = 0
        elif y == 3:
            Y0 = 1 - x
            z = 1
        elif y == 4:
            Y0 = 1 - x
            z = 1
        else:
            Y0 = 0
            z = 0

        result.append({'Y0': Y0, 'z': z})

    return result

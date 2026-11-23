def reference(vectors):
    result = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        if y == 0 or y == 2:
            Y0 = x
        elif y == 1 or y == 3 or y == 4:
            Y0 = 1 - x
        else:
            Y0 = 0
        z = 1 if y == 3 or y == 4 else 0
        result.append({'Y0': Y0, 'z': z})
    return result

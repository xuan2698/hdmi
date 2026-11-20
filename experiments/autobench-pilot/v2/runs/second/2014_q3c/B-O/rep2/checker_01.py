def reference(vectors):
    results = []
    for v in vectors:
        x = v['x'] & 1
        y = v['y'] & 7
        if y == 0:
            Y = 0 if x == 0 else 1
            z = 0
        elif y == 1:
            Y = 1 if x == 0 else 4
            z = 0
        elif y == 2:
            Y = 2 if x == 0 else 1
            z = 0
        elif y == 3:
            Y = 1 if x == 0 else 2
            z = 1
        elif y == 4:
            Y = 3 if x == 0 else 4
            z = 1
        else:
            Y = 0
            z = 0
        results.append({'Y0': Y & 1, 'z': z & 1})
    return results

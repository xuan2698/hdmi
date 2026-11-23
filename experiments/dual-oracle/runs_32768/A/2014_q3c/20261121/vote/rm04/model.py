def reference(vectors):
    next_y0 = {
        (0, 0): 0, (0, 1): 1, (0, 2): 0, (0, 3): 1, (0, 4): 1,
        (1, 0): 1, (1, 1): 0, (1, 2): 1, (1, 3): 0, (1, 4): 0,
    }
    zmap = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}
    result = []
    for row in vectors:
        x = int(row['x']) & 1
        y = int(row['y']) & 7
        result.append({
            'Y0': next_y0.get((x, y), 0),
            'z': zmap.get(y, 0),
        })
    return result

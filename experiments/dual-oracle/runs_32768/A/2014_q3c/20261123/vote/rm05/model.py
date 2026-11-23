def reference(vectors):
    table = {
        0: (0, 1, 0),
        1: (1, 0, 0),
        2: (0, 1, 0),
        3: (1, 0, 1),
        4: (1, 0, 1),
    }
    result = []
    for row in vectors:
        x = int(row["x"]) & 1
        y = int(row["y"]) & 7
        if y in table:
            y0_x0, y0_x1, z = table[y]
            y0 = y0_x1 if x else y0_x0
        else:
            y0 = 0
            z = 0
        result.append({"Y0": y0, "z": z})
    return result

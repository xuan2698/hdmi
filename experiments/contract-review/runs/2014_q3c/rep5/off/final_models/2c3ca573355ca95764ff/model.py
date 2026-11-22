def reference(vectors):
    # R_Y0 / R_z: combinational next-state bit 0 and output z from present state y and input x.
    # State-assigned table:
    #   y=000: x=0 -> Y=000 (Y0=0), x=1 -> Y=001 (Y0=1); z=0
    #   y=001: x=0 -> Y=001 (Y0=1), x=1 -> Y=100 (Y0=0); z=0
    #   y=010: x=0 -> Y=010 (Y0=0), x=1 -> Y=001 (Y0=1); z=0
    #   y=011: x=0 -> Y=001 (Y0=1), x=1 -> Y=010 (Y0=0); z=1
    #   y=100: x=0 -> Y=011 (Y0=1), x=1 -> Y=100 (Y0=0); z=1
    # Undefined states 101,110,111: don't-care -> Y0=0, z=0 (global uncertain interpretation).
    next_y0 = {
        0: {0: 0, 1: 1},
        1: {0: 1, 1: 0},
        2: {0: 0, 1: 1},
        3: {0: 1, 1: 0},
        4: {0: 1, 1: 0},
    }
    z_table = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}

    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 7
        if y in next_y0:
            Y0 = next_y0[y][x]
            z = z_table[y]
        else:
            # global: undefined states resolved as don't-care producing Y0=0, z=0
            Y0 = 0
            z = 0
        results.append({"Y0": Y0, "z": z})
    return results

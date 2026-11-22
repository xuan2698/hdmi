def reference(vectors):
    # R_Y0, R_z: combinational next-state bit 0 and output z from present state y and input x.
    # State-assigned table:
    #   y=000: x=0 -> Y=000 (Y0=0), x=1 -> Y=001 (Y0=1); z=0
    #   y=001: x=0 -> Y=001 (Y0=1), x=1 -> Y=100 (Y0=0); z=0
    #   y=010: x=0 -> Y=010 (Y0=0), x=1 -> Y=001 (Y0=1); z=0
    #   y=011: x=0 -> Y=001 (Y0=1), x=1 -> Y=010 (Y0=0); z=1
    #   y=100: x=0 -> Y=011 (Y0=1), x=1 -> Y=100 (Y0=0); z=1
    #   y=101,110,111: unspecified; treat as 0 outputs.
    next_Y0 = {
        0: {0: 0, 1: 1},
        1: {0: 1, 1: 0},
        2: {0: 0, 1: 1},
        3: {0: 1, 1: 0},
        4: {0: 1, 1: 0},
    }
    z_table = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}

    out = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 7
        # R_Y0: Y0 = next-state bit 0 as function of y and x per state-assigned table
        Y0 = next_Y0.get(y, {0: 0, 1: 0})[x]
        # R_z: z = 1 for present states 011 and 100, else 0
        z = z_table.get(y, 0)
        out.append({"Y0": Y0 & 1, "z": z & 1})
    return out

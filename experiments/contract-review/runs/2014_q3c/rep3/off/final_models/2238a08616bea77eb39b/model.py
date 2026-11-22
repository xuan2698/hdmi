def reference(vectors):
    # R_Y0, R_z: combinational logic from present state y and input x.
    # State-assigned table (only y=000..100 defined; others unspecified -> 0).
    # next-state bit 0 (Y0) per table:
    #   y=000: x=0 -> 000 (Y0=0), x=1 -> 001 (Y0=1)
    #   y=001: x=0 -> 001 (Y0=1), x=1 -> 100 (Y0=0)
    #   y=010: x=0 -> 010 (Y0=0), x=1 -> 001 (Y0=1)
    #   y=011: x=0 -> 001 (Y0=1), x=1 -> 010 (Y0=0)
    #   y=100: x=0 -> 011 (Y0=1), x=1 -> 100 (Y0=0)
    # z = 1 for y=011 or y=100, else 0.
    out = []
    for v in vectors:
        x = v["x"] & 1
        y = v["y"] & 7
        # R_Y0: next-state bit 0
        if y == 0:
            Y0 = 0 if x == 0 else 1
        elif y == 1:
            Y0 = 1 if x == 0 else 0
        elif y == 2:
            Y0 = 0 if x == 0 else 1
        elif y == 3:
            Y0 = 1 if x == 0 else 0
        elif y == 4:
            Y0 = 1 if x == 0 else 0
        else:
            Y0 = 0  # unspecified states -> 0
        # R_z: Moore output
        z = 1 if (y == 3 or y == 4) else 0
        out.append({"Y0": Y0 & 1, "z": z & 1})
    return out

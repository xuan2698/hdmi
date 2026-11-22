def reference(vectors):
    # Contract implementation.
    # R_Y0: Y0 = next-state bit 0 of Y[2:0] selected by x from present state y,
    #       for present states 000-100; states 101-111 unspecified.
    # R_z:  z = 1 when present state y is 011 or 100, else 0, for states 000-100;
    #       states 101-111 unspecified -> don't-care (interpretation chosen).
    # Timing: combinational, same_cycle. Each row's values driven before sampled edge.
    # Mid changes occur AFTER sampling, before other edge, carried to next row start.
    # No reset. Power-up unspecified -> return concrete unsigned ints.

    # Next-state table: for each present state y (0..4), (Y_x0, Y_x1)
    next_state = {
        0: (0b000, 0b001),
        1: (0b001, 0b100),
        2: (0b010, 0b001),
        3: (0b001, 0b010),
        4: (0b011, 0b100),
    }

    results = []
    for row in vectors:
        x = row["x"] & 1
        y = row["y"] & 0b111

        if y in next_state:
            Y = next_state[y][x]
            Y0 = Y & 1
            # R_z: z=1 for y==3 or y==4
            z = 1 if (y == 3 or y == 4) else 0
        else:
            # Unspecified states 101,110,111: don't-care.
            # R_z interpretation: z is don't-care -> choose 0.
            # R_Y0: don't-care -> choose 0.
            Y0 = 0
            z = 0

        results.append({"Y0": Y0 & 1, "z": z & 1})

    return results

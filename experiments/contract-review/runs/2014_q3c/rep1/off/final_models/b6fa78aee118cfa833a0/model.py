def reference(vectors):
    # State table: for each present state y (0..7), next state for x=0 and x=1
    # Only states 000-100 are specified; 101-111 unspecified.
    # R_Y0: Y0 = next-state bit 0 selected by x from present state y.
    # R_z: z = 1 when present state y is 011 or 100, else 0.
    # Unresolved R_z interpretation: z=1 for unspecified states 101,110,111.
    next_state = {
        0: (0, 1),  # 000 -> x=0:000, x=1:001
        1: (1, 4),  # 001 -> x=0:001, x=1:100
        2: (2, 1),  # 010 -> x=0:010, x=1:001
        3: (1, 2),  # 011 -> x=0:001, x=1:010
        4: (3, 4),  # 100 -> x=0:011, x=1:100
    }
    # Unspecified states 5,6,7: Y0 is don't-care; pick 0 (candidate interpretation).
    # z for unspecified states: z=1 per chosen interpretation.

    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 7

        # R_Y0: combinational next-state bit 0
        if y in next_state:
            ns = next_state[y][x]
            Y0 = ns & 1
        else:
            # unspecified state: Y0 don't-care -> choose 0
            Y0 = 0

        # R_z: combinational output
        if y in (3, 4):
            z = 1
        elif y in (5, 6, 7):
            # unresolved interpretation: z=1 for unspecified states
            z = 1
        else:
            z = 0

        results.append({"Y0": Y0 & 1, "z": z & 1})

    return results

def reference(vectors):
    # State-assigned table:
    # y=000: x=0 -> Y=000, x=1 -> Y=001
    # y=001: x=0 -> Y=001, x=1 -> Y=100
    # y=010: x=0 -> Y=010, x=1 -> Y=001
    # y=011: x=0 -> Y=001, x=1 -> Y=010
    # y=100: x=0 -> Y=011, x=1 -> Y=100
    # Unspecified 101,110,111: Y0 = 0 (don't-care, concrete choice)
    # z = 1 for y in {011, 100}, else 0

    # next_state[y][x] = Y[2:0]
    next_state = {
        0b000: (0b000, 0b001),
        0b001: (0b001, 0b100),
        0b010: (0b010, 0b001),
        0b011: (0b001, 0b010),
        0b100: (0b011, 0b100),
        0b101: (0b000, 0b000),  # don't-care -> Y0=0
        0b110: (0b000, 0b000),  # don't-care -> Y0=0
        0b111: (0b000, 0b000),  # don't-care -> Y0=0
    }

    results = []
    for vec in vectors:
        x = vec['x'] & 1
        y = vec['y'] & 0b111

        # R_Y0: Y0 = next-state bit 0 of Y[2:0] selected by x from present state y
        Y = next_state[y][x]
        Y0 = Y & 1

        # R_z: z = 1 when present state y is 011 or 100, else 0
        z = 1 if y in (0b011, 0b100) else 0

        results.append({'Y0': Y0, 'z': z})

    return results

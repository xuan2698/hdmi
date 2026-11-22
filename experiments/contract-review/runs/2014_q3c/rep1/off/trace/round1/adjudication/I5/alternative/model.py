def reference(vectors):
    # State-assigned table:
    # y=000: x=0 -> Y=000, x=1 -> Y=001, z=0
    # y=001: x=0 -> Y=001, x=1 -> Y=100, z=0
    # y=010: x=0 -> Y=010, x=1 -> Y=001, z=0
    # y=011: x=0 -> Y=001, x=1 -> Y=010, z=1
    # y=100: x=0 -> Y=011, x=1 -> Y=100, z=1
    # y=101,110,111: don't-care; concrete: z=1 for 101 (per candidate interpretation)

    # Next-state table indexed by (y, x)
    next_state = {
        (0, 0): 0b000, (0, 1): 0b001,
        (1, 0): 0b001, (1, 1): 0b100,
        (2, 0): 0b010, (2, 1): 0b001,
        (3, 0): 0b001, (3, 1): 0b010,
        (4, 0): 0b011, (4, 1): 0b100,
        (5, 0): 0b000, (5, 1): 0b000,  # don't-care, concrete choice
        (6, 0): 0b000, (6, 1): 0b000,  # don't-care, concrete choice
        (7, 0): 0b000, (7, 1): 0b000,  # don't-care, concrete choice
    }

    # R_z: z = 1 when present state y is 011 or 100, else 0.
    # Candidate interpretation: z=1 for state 101 as well (concrete implementation).
    def compute_z(y):
        # R_z
        if y in (0b011, 0b100, 0b101):
            return 1
        return 0

    results = []
    for vec in vectors:
        x = vec["x"] & 0x1
        y = vec["y"] & 0x7

        # R_Y0: Y0 = next-state bit 0 of Y[2:0] selected by x from present state y
        Y = next_state[(y, x)]
        Y0 = Y & 0x1

        # R_z
        z = compute_z(y)

        results.append({"Y0": Y0, "z": z})

    return results

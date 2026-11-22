def reference(vectors):
    # R_Y0: Y0 = LSB of next state selected by (y, x) per table.
    # R_z: z = 1 for y in {011, 100}; z = 0 for y in {000,001,010};
    #      z is don't-care for undefined states (y in {101,110,111}) -> use 0.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # No reset; power-up unspecified but we output concrete values each row.

    # Next-state table: next_state[y][x] -> 3-bit value
    next_state = {
        0b000: {0: 0b000, 1: 0b001},
        0b001: {0: 0b001, 1: 0b100},
        0b010: {0: 0b010, 1: 0b001},
        0b011: {0: 0b001, 1: 0b010},
        0b100: {0: 0b011, 1: 0b100},
    }

    def z_of(y):
        # R_z: defined states
        if y in (0b011, 0b100):
            return 1
        if y in (0b000, 0b001, 0b010):
            return 0
        # undefined states: don't-care -> concrete 0
        return 0

    def y0_of(y, x):
        # R_Y0: LSB of next state
        if y in next_state:
            return next_state[y][x] & 1
        # undefined states: don't-care -> concrete 0
        return 0

    results = []
    for row in vectors:
        x = row["x"] & 1
        y = row["y"] & 0b111
        results.append({"Y0": y0_of(y, x), "z": z_of(y)})
    return results

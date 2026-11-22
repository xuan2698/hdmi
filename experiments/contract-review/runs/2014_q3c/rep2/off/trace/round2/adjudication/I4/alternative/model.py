def reference(vectors):
    # Contract implementation.
    # R_Y0: Y0 = LSB of next state selected by (y, x) per table.
    # R_z: z = 1 for y in {011, 100}; z = 0 otherwise (including undefined 101,110,111).
    # Mid changes: applied after sampling, carried to next row (handled by caller-provided x/y per row).
    # No reset; outputs are combinational from current y and x.

    # Next-state table: next_state[y][x] -> 3-bit next state
    # y=000 -> x0:000, x1:001
    # y=001 -> x0:001, x1:100
    # y=010 -> x0:010, x1:001
    # y=011 -> x0:001, x1:010
    # y=100 -> x0:011, x1:100
    # y=101,110,111 -> unspecified; use Y0=0 (candidate interpretation for R_Y0)
    next_state = {
        0: {0: 0b000, 1: 0b001},
        1: {0: 0b001, 1: 0b100},
        2: {0: 0b010, 1: 0b001},
        3: {0: 0b001, 1: 0b010},
        4: {0: 0b011, 1: 0b100},
        5: {0: 0b000, 1: 0b000},  # undefined -> Y0=0
        6: {0: 0b000, 1: 0b000},  # undefined -> Y0=0
        7: {0: 0b000, 1: 0b000},  # undefined -> Y0=0
    }

    results = []
    for row in vectors:
        x = row.get('x', 0) & 1
        y = row.get('y', 0) & 0b111

        # R_Y0: combinational next-state LSB
        ns = next_state[y][x]
        Y0 = ns & 1

        # R_z: z=1 for y=011 or y=100, else 0 (including undefined states)
        z = 1 if y in (0b011, 0b100) else 0

        results.append({'Y0': Y0, 'z': z})

    return results

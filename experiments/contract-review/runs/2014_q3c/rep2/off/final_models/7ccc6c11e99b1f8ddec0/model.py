def reference(vectors):
    # Contract rules:
    # R_Y0: Y0 = LSB of next state selected by (y, x) per table.
    # R_z: z = 1 for y in {011, 100}; z = 0 otherwise (including undefined 101,110,111).
    # Mid changes occur AFTER sampling, before other edge, carried to next row start.
    # No reset; power-up unspecified but we output concrete values each row.

    # Next-state table: next_state[y][x] -> Y[2:0]
    # y=000: x0->000, x1->001
    # y=001: x0->001, x1->100
    # y=010: x0->010, x1->001
    # y=011: x0->001, x1->010
    # y=100: x0->011, x1->100
    # y=101,110,111: undefined -> treat Y0 as 0 (candidate interpretation)
    next_state = {
        0b000: {0: 0b000, 1: 0b001},
        0b001: {0: 0b001, 1: 0b100},
        0b010: {0: 0b010, 1: 0b001},
        0b011: {0: 0b001, 1: 0b010},
        0b100: {0: 0b011, 1: 0b100},
    }

    results = []
    # State carried across rows (present state y). Power-up unspecified; start at 0.
    y = 0

    for vec in vectors:
        x = vec.get('x', 0) & 1
        # If vector explicitly provides y, use it as the present state for this row.
        if 'y' in vec:
            y = vec['y'] & 0b111

        # R_Y0: compute next state, take LSB.
        if y in next_state:
            ns = next_state[y][x]
        else:
            ns = 0  # undefined states -> Y0 = 0 (candidate interpretation)
        Y0 = ns & 1

        # R_z: z = 1 for y in {011, 100}, else 0 (including undefined).
        z = 1 if y in (0b011, 0b100) else 0

        results.append({'Y0': Y0, 'z': z})

        # State update on posedge clk: present state becomes next state.
        # (Sampling happens at edge; mid changes after sampling affect next row.)
        y = ns

    return results

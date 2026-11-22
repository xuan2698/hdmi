def reference(vectors):
    # Contract rules implemented:
    # R_Y0: Y0 = next-state bit 0, combinational from present state y and input x.
    # R_z: z = 1 when present state y is 011 or 100, else 0 (Moore output).
    # global: undefined states y=101,110,111 -> Y0=0, z=1 (chosen candidate).
    # mid: mid input changes occur after sampling, carried to next row.
    # No reset. Sample after posedge settled; each row's values driven before sampled edge.

    # State-assigned table: next state Y[2:0] for (y, x)
    # y=000: x=0 -> 000, x=1 -> 001
    # y=001: x=0 -> 001, x=1 -> 100
    # y=010: x=0 -> 010, x=1 -> 001
    # y=011: x=0 -> 001, x=1 -> 010
    # y=100: x=0 -> 011, x=1 -> 100
    # y=101,110,111: undefined -> Y0=0 (per chosen candidate)

    next_state = {
        0: {0: 0b000, 1: 0b001},
        1: {0: 0b001, 1: 0b100},
        2: {0: 0b010, 1: 0b001},
        3: {0: 0b001, 1: 0b010},
        4: {0: 0b011, 1: 0b100},
    }

    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 0b111

        # R_z: Moore output from present state
        if y == 0b011 or y == 0b100:
            z = 1
        elif y in (0b101, 0b110, 0b111):
            # global: undefined states -> z=1
            z = 1
        else:
            z = 0

        # R_Y0: next-state bit 0
        if y in next_state:
            ns = next_state[y][x]
            Y0 = ns & 1
        else:
            # global: undefined states -> Y0=0
            Y0 = 0

        results.append({"Y0": Y0, "z": z})

    return results

def reference(vectors):
    # State-assigned table:
    # y=000: x0->000, x1->001
    # y=001: x0->001, x1->100
    # y=010: x0->010, x1->001
    # y=011: x0->001, x1->010
    # y=100: x0->011, x1->100
    # undefined states (101,110,111): don't-care -> Y0=0, z=0

    # R_Y0: Y0 = LSB of next state selected by (y, x)
    # R_z: z = 1 if y in {011, 100} else 0

    next_state = {
        (0b000, 0): 0b000, (0b000, 1): 0b001,
        (0b001, 0): 0b001, (0b001, 1): 0b100,
        (0b010, 0): 0b010, (0b010, 1): 0b001,
        (0b011, 0): 0b001, (0b011, 1): 0b010,
        (0b100, 0): 0b011, (0b100, 1): 0b100,
    }

    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 0b111

        # R_Y0: combinational, same cycle
        ns = next_state.get((y, x))
        if ns is None:
            Y0 = 0  # don't-care interpretation
        else:
            Y0 = ns & 1

        # R_z: combinational, same cycle
        z = 1 if y in (0b011, 0b100) else 0

        results.append({"Y0": Y0, "z": z})

    return results

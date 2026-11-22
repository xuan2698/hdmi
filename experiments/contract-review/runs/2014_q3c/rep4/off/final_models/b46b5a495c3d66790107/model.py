def reference(vectors):
    # State-assigned table:
    # y=000 -> x=0: Y=000, x=1: Y=001, z=0
    # y=001 -> x=0: Y=001, x=1: Y=100, z=0
    # y=010 -> x=0: Y=010, x=1: Y=001, z=0
    # y=011 -> x=0: Y=001, x=1: Y=010, z=1
    # y=100 -> x=0: Y=011, x=1: Y=100, z=1
    # Undefined states 101,110,111 -> Y0=0, z=0 (per chosen interpretation)

    # R_Y0: Y0 = next-state bit 0 of Y[2:0] per table (combinational, same_cycle)
    # R_z: z = 1 when present state y is 011 or 100, else 0 (Moore output)
    #      (chosen interpretation: Moore, not Mealy)

    # next-state table: key = (y, x) -> Y[2:0]
    next_state = {
        (0b000, 0): 0b000,
        (0b000, 1): 0b001,
        (0b001, 0): 0b001,
        (0b001, 1): 0b100,
        (0b010, 0): 0b010,
        (0b010, 1): 0b001,
        (0b011, 0): 0b001,
        (0b011, 1): 0b010,
        (0b100, 0): 0b011,
        (0b100, 1): 0b100,
    }

    results = []
    for vec in vectors:
        x = vec.get('x', 0) & 1
        y = vec.get('y', 0) & 0b111

        # R_Y0: combinational next-state bit 0
        if (y, x) in next_state:
            Y = next_state[(y, x)]
            Y0 = Y & 1
        else:
            # Undefined states 101,110,111 -> Y0=0
            Y0 = 0

        # R_z: Moore output from present state
        if y in (0b011, 0b100):
            z = 1
        else:
            z = 0

        results.append({'Y0': Y0, 'z': z})

    return results

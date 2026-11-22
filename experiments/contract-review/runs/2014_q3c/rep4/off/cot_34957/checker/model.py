def reference(vectors):
    # State-assigned table:
    # y=000: x=0 -> Y=000, x=1 -> Y=001, z=0
    # y=001: x=0 -> Y=001, x=1 -> Y=100, z=0
    # y=010: x=0 -> Y=010, x=1 -> Y=001, z=0
    # y=011: x=0 -> Y=001, x=1 -> Y=010, z=1
    # y=100: x=0 -> Y=011, x=1 -> Y=100, z=1
    #
    # Y[0] is the LSB of the next state.
    # z depends only on present state y.
    #
    # Contract: Y[0] uses pre-edge captured x with driven y.
    # z depends only on y. Skip unlisted y and before legal y driven.

    # next_state_lsb[y][x] -> Y[0]
    next_lsb = {
        0b000: {0: 0, 1: 1},
        0b001: {0: 1, 1: 0},
        0b010: {0: 0, 1: 1},
        0b011: {0: 1, 1: 0},
        0b100: {0: 1, 1: 0},
    }
    # output z by present state
    z_map = {
        0b000: 0,
        0b001: 0,
        0b010: 0,
        0b011: 1,
        0b100: 1,
    }

    results = []
    for row in vectors:
        y = row.get('y')
        x = row.get('x')
        out = {}
        if y is not None and y in next_lsb and x is not None:
            out['Y0'] = next_lsb[y][x]
            out['z'] = z_map[y]
        else:
            # Skip checks: no legal y driven yet or unlisted y.
            # Still must return concrete unsigned integers within bit width.
            out['Y0'] = 0
            out['z'] = 0
        results.append(out)
    return results

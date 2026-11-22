def reference(vectors):
    # State table: next state for (y, x)
    # y=000: x0->000, x1->001
    # y=001: x0->001, x1->100
    # y=010: x0->010, x1->001
    # y=011: x0->001, x1->010
    # y=100: x0->011, x1->100
    # y=101,110,111: unspecified -> default Y0=0, z=0
    next_state = {
        (0, 0): 0, (0, 1): 1,
        (1, 0): 1, (1, 1): 4,
        (2, 0): 2, (2, 1): 1,
        (3, 0): 1, (3, 1): 2,
        (4, 0): 3, (4, 1): 4,
    }
    results = []
    for row in vectors:
        x = row['x'] & 1
        y = row['y'] & 7
        # R_Y0: Y0 = LSB of next state selected by (y, x)
        ns = next_state.get((y, x), 0)
        Y0 = ns & 1
        # R_z: z = 1 when y is 011 or 100, else 0
        z = 1 if y in (3, 4) else 0
        results.append({'Y0': Y0, 'z': z})
    return results

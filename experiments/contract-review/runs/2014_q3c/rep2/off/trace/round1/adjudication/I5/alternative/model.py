def reference(vectors):
    # State table: next state Y[2:0] given (y, x)
    # y=000: x0->000, x1->001
    # y=001: x0->001, x1->100
    # y=010: x0->010, x1->001
    # y=011: x0->001, x1->010
    # y=100: x0->011, x1->100
    next_state = {
        (0, 0): 0, (0, 1): 1,
        (1, 0): 1, (1, 1): 4,
        (2, 0): 2, (2, 1): 1,
        (3, 0): 1, (3, 1): 2,
        (4, 0): 3, (4, 1): 4,
    }
    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 7
        Y = next_state.get((y, x), 0)
        # R_Y0: Y0 is LSB of next state
        Y0 = Y & 1
        # R_z: z=1 for states 011 or 100, else 0 (including undefined states -> 0)
        z = 1 if y in (3, 4) else 0
        results.append({"Y0": Y0, "z": z})
    return results

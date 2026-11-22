def reference(vectors):
    # State-assigned table: next state Y[2:0] as function of (y, x)
    # y=000: x=0->000, x=1->001
    # y=001: x=0->001, x=1->100
    # y=010: x=0->010, x=1->001
    # y=011: x=0->001, x=1->010
    # y=100: x=0->011, x=1->100
    # Undefined states (101,110,111): next state 000 (Y0=0) per candidate interpretation
    next_state = {
        0: {0: 0, 1: 1},
        1: {0: 1, 1: 4},
        2: {0: 2, 1: 1},
        3: {0: 1, 1: 2},
        4: {0: 3, 1: 4},
    }
    # R_Y0: Y0 = next-state bit 0 as function of y and x per state-assigned table
    # R_z: z = 1 for present states 011 and 100, else 0
    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 7
        if y in next_state:
            ns = next_state[y][x]
        else:
            ns = 0  # undefined states -> next state 000
        Y0 = ns & 1
        z = 1 if (y == 3 or y == 4) else 0
        results.append({"Y0": Y0, "z": z})
    return results

def reference(vectors):
    # R_Y0: Y0 = next-state bit 0 as function of y and x per state-assigned table
    # R_z: z = 1 for present states 011 and 100, else 0
    # Undefined states 101,110,111 -> Y0=0, z=0 (uncertain resolution)
    # mid changes occur AFTER sampling, carried to start of next row
    results = []
    for vec in vectors:
        y = vec["y"] & 0x7
        x = vec["x"] & 0x1
        # R_z
        if y == 0b011 or y == 0b100:
            z = 1
        else:
            z = 0
        # R_Y0: next state bit 0
        if y == 0b000:
            nxt = 0b000 if x == 0 else 0b001
        elif y == 0b001:
            nxt = 0b001 if x == 0 else 0b100
        elif y == 0b010:
            nxt = 0b010 if x == 0 else 0b001
        elif y == 0b011:
            nxt = 0b001 if x == 0 else 0b010
        elif y == 0b100:
            nxt = 0b011 if x == 0 else 0b100
        else:
            nxt = 0b000  # don't-care resolution
        Y0 = nxt & 0x1
        results.append({"Y0": Y0, "z": z})
    return results

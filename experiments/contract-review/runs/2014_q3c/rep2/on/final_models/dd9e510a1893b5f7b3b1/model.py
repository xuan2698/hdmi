def reference(vectors):
    result = []
    for v in vectors:
        x = v["x"] & 1
        y = v["y"] & 7
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1

        # Rule valid_y_0_to_4: combinational Y0 and z, visible same_cycle.
        # Y0 is next-state bit 0; concrete values are produced for all y.
        not_x = 1 ^ x
        not_y0 = 1 ^ y0
        not_y2 = 1 ^ y2
        Y0 = (not_x & y0) | (not_x & y2) | (x & not_y2 & not_y0)
        z = y2 | (y1 & y0)

        result.append({"Y0": Y0 & 1, "z": z & 1})
    return result

def reference(vectors):
    out = []
    for row in vectors:
        x = row["x"] & 1
        y = row["y"] & 7
        y2 = (y >> 2) & 1
        y1 = (y >> 1) & 1
        y0 = y & 1
        Y0 = x ^ (y2 | y0)
        z = y2 | (y1 & y0)
        out.append({"Y0": Y0, "z": z})
    return out

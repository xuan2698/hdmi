def reference(vectors):
    out = []
    for row in vectors:
        x = int(row["x"]) & 1
        y = int(row["y"]) & 7
        a = (y >> 2) & 1
        b = (y >> 1) & 1
        c = y & 1
        y0 = ((1 - x) & (a | c)) | (x & (1 - a) & (1 - c))
        z = a | (b & c)
        out.append({"Y0": y0 & 1, "z": z & 1})
    return out

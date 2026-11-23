def reference(vectors):
    result = []
    for v in vectors:
        x = v["x"] & 1
        y = v["y"] & 7
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1
        result.append({
            "Y0": x ^ (y2 | y0),
            "z": y2 | (y1 & y0)
        })
    return result

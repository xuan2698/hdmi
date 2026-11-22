def reference(vectors):
    # sync_reset: at a sampled posedge, r == 1 forces q to 0
    # d_load: at a sampled posedge, r == 0 causes q to capture d
    cur = {"d": 0, "r": 0}
    out = []
    for row in vectors:
        for k in row:
            if k != "mid":
                cur[k] = row[k]
        d = cur["d"]
        r = cur["r"]
        if r:
            q = 0  # sync_reset
        else:
            q = 1 if d else 0  # d_load
        out.append({"q": q})
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                cur.update(mid)
    return out

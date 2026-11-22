def reference(vectors):
    # Registered 8-bit D flip-flop output.
    q = 0
    # Current input values, including carried mid changes.
    cur = {"d": 0, "reset": 0}
    widths = {"d": 8, "reset": 1}
    out = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        for k, v in row.items():
            if k == "mid":
                continue
            if k in widths:
                cur[k] = int(v) & ((1 << widths[k]) - 1)
            else:
                cur[k] = v

        if (cur.get("reset", 0) & 1) == 1:
            # sync_reset_high: active-high synchronous reset clears q to zero.
            q = 0
        else:
            # dff_load_d: on posedge with reset low, load d into q.
            q = int(cur.get("d", 0)) & 0xFF

        out.append({"q": q & 0xFF})

        # Optional mid input changes occur after sampling and are carried forward.
        mid = row.get("mid")
        if mid:
            for k, v in mid.items():
                if k in widths:
                    cur[k] = int(v) & ((1 << widths[k]) - 1)
                else:
                    cur[k] = v

    return out

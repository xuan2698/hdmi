def reference(vectors):
    q = 0
    d_now = 0
    r_now = 0
    result = []

    for row in vectors:
        # Apply inputs driven before the sampled posedge.
        # Carried mid changes remain unless overridden by this row.
        if "d" in row:
            d_now = row["d"] & 1
        if "r" in row:
            r_now = row["r"] & 1

        # Rule sync_reset: at a sampled posedge, r == 1 forces q to 0.
        # Rule d_load: at a sampled posedge, r == 0 makes q capture d.
        if r_now == 1:
            q = 0
        else:
            q = d_now & 1

        result.append({"q": q & 1})

        # Apply mid changes AFTER sampling. They are carried to the next row
        # and do not affect the already sampled q.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                try:
                    items = mid.items()
                    for k, v in items:
                        if k == "d":
                            d_now = v & 1
                        elif k == "r":
                            r_now = v & 1
                except AttributeError:
                    try:
                        for change in mid:
                            try:
                                items = change.items()
                                for k, v in items:
                                    if k == "d":
                                        d_now = v & 1
                                    elif k == "r":
                                        r_now = v & 1
                            except AttributeError:
                                pass
                    except TypeError:
                        pass

    return result

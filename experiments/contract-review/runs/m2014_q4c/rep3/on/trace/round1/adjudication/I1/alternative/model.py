def reference(vectors):
    # global: negative-edge-triggered D flip-flop with synchronous active-high reset on negedge clk.
    q = 0
    carried_d = 0
    carried_r = 0
    result = []

    for row in vectors:
        # Apply row values driven before the sampled negedge; omitted inputs retain carried values.
        try:
            carried_d = row["d"] & 1
        except:
            try:
                carried_d = row[0] & 1
            except:
                pass

        try:
            carried_r = row["r"] & 1
        except:
            try:
                carried_r = row[1] & 1
            except:
                pass

        # sync_active_high_reset: at sampled negedge, r == 1 forces q to 0 regardless of d.
        # d_capture_when_not_reset: at sampled negedge, r == 0 captures d into q.
        if carried_r == 1:
            q = 0
        else:
            q = carried_d & 1

        result.append({"q": q})

        # Mid changes occur after sampling and are carried to the start of the next row.
        try:
            mid = row["mid"]
        except:
            mid = None

        if mid is not None:
            applied = False
            try:
                carried_d = mid["d"] & 1
                applied = True
            except:
                pass
            try:
                carried_r = mid["r"] & 1
                applied = True
            except:
                pass

            if not applied:
                try:
                    for change in mid:
                        try:
                            carried_d = change["d"] & 1
                        except:
                            pass
                        try:
                            carried_r = change["r"] & 1
                        except:
                            pass
                except:
                    pass

    return result

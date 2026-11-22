def reference(vectors):
    result = []
    cur_x = 0
    cur_y = 0
    for vec in vectors:
        # Drive row values before the sampled posedge.
        if "x" in vec:
            cur_x = vec["x"]
        if "y" in vec:
            cur_y = vec["y"]

        x = cur_x
        y = cur_y
        y0 = y & 1
        y1 = (y >> 1) & 1
        y2 = (y >> 2) & 1

        # valid_y_0_to_4: minimized Y0 and z expressions.
        if x == 0:
            Y0 = y0 | y2
        else:
            Y0 = (1 - y2) & (1 - y0)
        z = y2 | (y1 & y0)
        result.append({"Y0": Y0 & 1, "z": z & 1})

        # global: unused present states y=5,6,7 are evaluated with the
        # minimized expressions selected by the don't-care interpretation.
        # Mid changes occur after sampling and carry to the start of the next row.
        if "mid" in vec:
            mid = vec["mid"]
            if mid is not None:
                try:
                    if "x" in mid:
                        cur_x = mid["x"]
                    if "y" in mid:
                        cur_y = mid["y"]
                except:
                    try:
                        for change in mid:
                            if "x" in change:
                                cur_x = change["x"]
                            if "y" in change:
                                cur_y = change["y"]
                    except:
                        pass
        if "mid_x" in vec:
            cur_x = vec["mid_x"]
        if "mid_y" in vec:
            cur_y = vec["mid_y"]
        if "x_mid" in vec:
            cur_x = vec["x_mid"]
        if "y_mid" in vec:
            cur_y = vec["y_mid"]

    return result

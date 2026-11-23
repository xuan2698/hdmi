def reference(vectors):
    state = "WL"
    fall_count = 0
    outputs = []
    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        if areset:
            state = "WL"
            fall_count = 0
        else:
            if state == "WL":
                if not ground:
                    state = "FL"
                    fall_count = 0
                elif dig:
                    state = "DL"
                elif bump_left:
                    state = "WR"
            elif state == "WR":
                if not ground:
                    state = "FR"
                    fall_count = 0
                elif dig:
                    state = "DR"
                elif bump_right:
                    state = "WL"
            elif state == "DL":
                if not ground:
                    state = "FL"
                    fall_count = 0
            elif state == "DR":
                if not ground:
                    state = "FR"
                    fall_count = 0
            elif state == "FL":
                if ground:
                    if fall_count >= 20:
                        state = "DEAD"
                    else:
                        state = "WL"
                    fall_count = 0
                else:
                    fall_count += 1
            elif state == "FR":
                if ground:
                    if fall_count >= 20:
                        state = "DEAD"
                    else:
                        state = "WR"
                    fall_count = 0
                else:
                    fall_count += 1
            elif state == "DEAD":
                fall_count = 0

        if state == "WL":
            wl, wr, aa, dg = 1, 0, 0, 0
        elif state == "WR":
            wl, wr, aa, dg = 0, 1, 0, 0
        elif state == "FL" or state == "FR":
            wl, wr, aa, dg = 0, 0, 1, 0
        elif state == "DL" or state == "DR":
            wl, wr, aa, dg = 0, 0, 0, 1
        else:
            wl, wr, aa, dg = 0, 0, 0, 0

        outputs.append({
            "walk_left": wl,
            "walk_right": wr,
            "aaah": aa,
            "digging": dg
        })

    return outputs

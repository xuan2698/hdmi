def reference(vectors):
    state = "LEFT"
    counter = 0
    out = []
    for v in vectors:
        areset = v["areset"]
        bump_left = v["bump_left"]
        bump_right = v["bump_right"]
        ground = v["ground"]
        dig = v["dig"]

        if areset:
            state = "LEFT"
            counter = 0
        elif state == "DEAD":
            pass
        elif state == "LEFT" or state == "RIGHT":
            if ground == 0:
                state = "FALL_L" if state == "LEFT" else "FALL_R"
                counter = 1
            elif dig == 1:
                state = "DIG_L" if state == "LEFT" else "DIG_R"
                counter = 0
            else:
                if bump_left and bump_right:
                    state = "RIGHT" if state == "LEFT" else "LEFT"
                elif bump_left:
                    state = "RIGHT"
                elif bump_right:
                    state = "LEFT"
                counter = 0
        elif state == "DIG_L" or state == "DIG_R":
            if ground == 0:
                state = "FALL_L" if state == "DIG_L" else "FALL_R"
                counter = 1
        elif state == "FALL_L" or state == "FALL_R":
            if ground == 0:
                counter += 1
            else:
                if counter > 20:
                    state = "DEAD"
                else:
                    state = "LEFT" if state == "FALL_L" else "RIGHT"
                counter = 0

        out.append({
            "walk_left": 1 if state == "LEFT" else 0,
            "walk_right": 1 if state == "RIGHT" else 0,
            "aaah": 1 if state == "FALL_L" or state == "FALL_R" else 0,
            "digging": 1 if state == "DIG_L" or state == "DIG_R" else 0,
        })
    return out

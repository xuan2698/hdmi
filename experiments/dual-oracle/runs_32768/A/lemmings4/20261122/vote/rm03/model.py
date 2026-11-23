def reference(vectors):
    state = "WL"
    fall_count = 0
    result = []
    for v in vectors:
        if v["areset"]:
            state = "WL"
            fall_count = 0
        else:
            ground = v["ground"]
            dig = v["dig"]
            bump_left = v["bump_left"]
            bump_right = v["bump_right"]

            if state == "WL":
                if not ground:
                    state = "FL"
                    fall_count = 1
                elif dig:
                    state = "DL"
                    fall_count = 0
                else:
                    state = "WR" if bump_left else "WL"
                    fall_count = 0
            elif state == "WR":
                if not ground:
                    state = "FR"
                    fall_count = 1
                elif dig:
                    state = "DR"
                    fall_count = 0
                else:
                    state = "WL" if bump_right else "WR"
                    fall_count = 0
            elif state == "DL":
                if not ground:
                    state = "FL"
                    fall_count = 1
                else:
                    state = "DL"
                    fall_count = 0
            elif state == "DR":
                if not ground:
                    state = "FR"
                    fall_count = 1
                else:
                    state = "DR"
                    fall_count = 0
            elif state == "FL":
                if ground:
                    if fall_count > 20:
                        state = "DEAD"
                    else:
                        state = "WL"
                    fall_count = 0
                else:
                    fall_count += 1
                    state = "FL"
            elif state == "FR":
                if ground:
                    if fall_count > 20:
                        state = "DEAD"
                    else:
                        state = "WR"
                    fall_count = 0
                else:
                    fall_count += 1
                    state = "FR"
            else:
                state = "DEAD"
                fall_count = 0

        if state == "WL":
            result.append({"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0})
        elif state == "WR":
            result.append({"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0})
        elif state == "FL" or state == "FR":
            result.append({"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0})
        elif state == "DL" or state == "DR":
            result.append({"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1})
        else:
            result.append({"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0})
    return result

def reference(vectors):
    WL, WR, DL, DR, FL, FR, SP = 0, 1, 2, 3, 4, 5, 6
    state = WL
    fall_count = 0
    result = []

    for row in vectors:
        if isinstance(row, dict):
            ar = row.get('areset', 0)
            bl = row.get('bump_left', 0)
            br = row.get('bump_right', 0)
            gr = row.get('ground', 0)
            dg = row.get('dig', 0)
        else:
            ar, bl, br, gr, dg = row

        if ar:
            state = WL
            fall_count = 0
        elif state == SP:
            pass
        elif state == FL or state == FR:
            left = (state == FL)
            if gr == 0:
                fall_count += 1
            else:
                if fall_count > 20:
                    state = SP
                    fall_count = 0
                else:
                    state = WL if left else WR
                    fall_count = 0
        elif state == WL or state == WR:
            if gr == 0:
                state = FL if state == WL else FR
                fall_count = 1
            else:
                if dg:
                    state = DL if state == WL else DR
                    fall_count = 0
                else:
                    if bl and br:
                        state = WR if state == WL else WL
                    elif bl:
                        state = WR
                    elif br:
                        state = WL
                    fall_count = 0
        elif state == DL or state == DR:
            if gr == 0:
                state = FL if state == DL else FR
                fall_count = 1

        if state == WL:
            walk_left, walk_right, aaah, digging = 1, 0, 0, 0
        elif state == WR:
            walk_left, walk_right, aaah, digging = 0, 1, 0, 0
        elif state == DL or state == DR:
            walk_left, walk_right, aaah, digging = 0, 0, 0, 1
        elif state == FL or state == FR:
            walk_left, walk_right, aaah, digging = 0, 0, 1, 0
        else:
            walk_left, walk_right, aaah, digging = 0, 0, 0, 0

        result.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })

    return result
